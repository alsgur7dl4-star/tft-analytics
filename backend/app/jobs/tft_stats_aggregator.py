from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.comp_stats import assign_tier_label, calculate_comp_score
from app.models.tft import TftComp, TftCompStatsDaily, TftMatch, TftMatchParticipant


def _trait_fingerprint(traits_json: list[dict]) -> str | None:
    """활성 시너지 상위 3개를 정렬해 조합 식별키 생성."""
    active = [
        (t["name"], t.get("num_units", 0))
        for t in traits_json
        if t.get("style", 0) > 0 and t.get("name")
    ]
    if not active:
        return None
    active.sort(key=lambda x: -x[1])
    return " / ".join(sorted(name for name, _ in active[:3]))


def _core_units(units_json: list[dict]) -> list[str]:
    """별 수 높은 순으로 상위 5기물 추출."""
    ranked = sorted(units_json, key=lambda u: u.get("tier", 0), reverse=True)
    return [u.get("character_id") or u.get("name", "") for u in ranked[:5] if u.get("character_id") or u.get("name")]


def _active_traits(traits_json: list[dict]) -> list[str]:
    return [t["name"] for t in traits_json if t.get("style", 0) > 0 and t.get("name")]


def _load_valid_tier_labels(db: Session) -> list[str]:
    """공통코드 TIER_LABEL 그룹에서 유효 티어 라벨 목록 조회."""
    from app.models.common import CommonCode, CommonCodeGroup
    group = db.scalar(select(CommonCodeGroup).where(CommonCodeGroup.group_key == "TIER_LABEL"))
    if not group:
        return ["S", "A", "B", "C", "D"]
    codes = db.scalars(
        select(CommonCode)
        .where(CommonCode.group_id == group.id)
        .order_by(CommonCode.sort_order.asc())
    ).all()
    return [c.code for c in codes] if codes else ["S", "A", "B", "C", "D"]


def recalculate_tft_stats(db: Session) -> dict[str, str]:
    # 공통코드에서 유효 티어 라벨 조회 (공통코드 활용 지점)
    valid_tier_labels = _load_valid_tier_labels(db)

    participants = list(
        db.scalars(
            select(TftMatchParticipant).where(TftMatchParticipant.traits_json.isnot(None))
        )
    )

    if not participants:
        return {"status": "SKIP", "message": "수집된 경기 데이터가 없습니다."}

    # 시너지 기반 조합 그룹핑
    groups: dict[str, list[TftMatchParticipant]] = defaultdict(list)
    for p in participants:
        fp = _trait_fingerprint(p.traits_json or [])
        if fp:
            groups[fp].append(p)

    total_games = len(participants)
    today = datetime.now(timezone.utc).date()

    # 그룹별 통계 계산 (표본 5경기 이상만)
    comp_data: dict[str, dict[str, Any]] = {}
    max_pick_rate = 0.0
    for fp, group in groups.items():
        if len(group) < 5:
            continue
        placements = [p.placement for p in group]
        games = len(placements)
        avg_placement = sum(placements) / games
        top4_rate = sum(1 for pl in placements if pl <= 4) / games
        first_rate = sum(1 for pl in placements if pl == 1) / games
        pick_rate = games / total_games
        max_pick_rate = max(max_pick_rate, pick_rate)
        comp_data[fp] = {
            "games": games,
            "avg_placement": avg_placement,
            "top4_rate": top4_rate,
            "first_rate": first_rate,
            "pick_rate": pick_rate,
            "sample": group[0],
        }

    if not comp_data:
        return {"status": "SKIP", "message": "통계 계산 가능한 조합이 없습니다 (최소 5경기 필요)."}

    # 점수 계산
    for fp, data in comp_data.items():
        data["score"] = calculate_comp_score(
            data["top4_rate"],
            data["first_rate"],
            data["pick_rate"],
            data["avg_placement"],
            max_pick_rate,
            data["games"],
            min_sample_count=5,
        )

    # 점수 순 정렬 후 공통코드 기반 티어 라벨 부여
    ranked = sorted(comp_data.keys(), key=lambda f: comp_data[f]["score"], reverse=True)
    total = len(ranked)
    for rank, fp in enumerate(ranked):
        label = assign_tier_label(rank / total)
        # 공통코드에 없는 라벨은 마지막 유효 라벨로 대체
        comp_data[fp]["tier_label"] = label if label in valid_tier_labels else valid_tier_labels[-1]

    # TftComp + TftCompStatsDaily upsert
    saved = 0
    for fp, data in comp_data.items():
        sample: TftMatchParticipant = data["sample"]
        match = db.get(TftMatch, sample.match_id)
        set_name = (match.set_name or "unknown") if match else "unknown"
        patch = (match.game_version or "latest") if match else "latest"

        units = _core_units(sample.units_json or [])
        traits = _active_traits(sample.traits_json or [])

        comp = db.scalar(select(TftComp).where(TftComp.comp_name == fp))
        if not comp:
            comp = TftComp(
                comp_name=fp,
                set_name=set_name,
                patch_version=patch,
                core_units_json=units,
                core_traits_json=traits,
                core_items_json=[],
            )
            db.add(comp)
        else:
            comp.core_units_json = units
            comp.core_traits_json = traits
            comp.patch_version = patch
        db.flush()

        existing = db.scalar(
            select(TftCompStatsDaily).where(
                TftCompStatsDaily.stat_date == today,
                TftCompStatsDaily.comp_id == comp.id,
                TftCompStatsDaily.region == "KR",
            )
        )
        stat_row = existing or TftCompStatsDaily(
            stat_date=today,
            set_name=set_name,
            patch_version=patch,
            region="KR",
            comp_id=comp.id,
        )
        stat_row.games = data["games"]
        stat_row.avg_placement = round(data["avg_placement"], 4)
        stat_row.top4_rate = round(data["top4_rate"], 4)
        stat_row.first_rate = round(data["first_rate"], 4)
        stat_row.pick_rate = round(data["pick_rate"], 4)
        stat_row.score = data["score"]
        stat_row.tier_label = data["tier_label"]
        stat_row.tier = data["tier_label"]
        db.add(stat_row)
        saved += 1

    db.flush()
    return {
        "status": "SUCCESS",
        "message": f"{saved}개 조합 통계 재계산 완료 (분석 경기: {total_games}경기)",
    }
