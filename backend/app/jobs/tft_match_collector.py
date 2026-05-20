import logging
import random

from sqlalchemy.orm import Session

from app.clients.riot_tft_client import RiotTftClient
from app.repositories.tft_repository import TftRepository

logger = logging.getLogger(__name__)


async def collect_top_elo_matches(
    db: Session,
    max_summoners: int = 30,
    matches_per_summoner: int = 10,
    region: str = "kr",
    routing: str = "asia",
) -> dict[str, int]:
    riot = RiotTftClient()
    repo = TftRepository(db)

    # 1. 챌린저 리그에서 소환사 목록 수집
    challenger = await riot.get_challenger_league(region)
    entries = challenger.get("entries", [])

    # 표본이 부족하면 그마도 추가
    if len(entries) < max_summoners:
        grandmaster = await riot.get_grandmaster_league(region)
        entries.extend(grandmaster.get("entries", []))

    sample = random.sample(entries, min(max_summoners, len(entries)))

    collected_summoners = 0
    collected_matches = 0
    skipped_matches = 0

    for entry in sample:
        # 최신 Riot API는 리그 엔트리에 puuid를 직접 포함 (summonerId 미반환)
        puuid = entry.get("puuid")
        if not puuid:
            continue

        # 2. puuid → Riot 계정 정보(gameName, tagLine) 조회
        try:
            account_data = await riot.get_account_by_puuid(puuid, routing)
            game_name = account_data.get("gameName") or puuid[:16]
            tag_line = account_data.get("tagLine") or "KR1"
        except Exception as exc:
            logger.warning("account fetch failed for puuid %s: %s", puuid, exc)
            game_name = puuid[:16]
            tag_line = "KR1"

        # 3. puuid → 소환사 데이터(level, iconId 등) 조회
        # 최신 Riot API는 summonerId(id)를 응답에서 제거했으므로 puuid를 식별자로 사용
        try:
            summoner_data = await riot.get_summoner_by_puuid(puuid, region)
        except Exception as exc:
            logger.warning("summoner fetch failed for puuid %s: %s", puuid, exc)
            summoner_data = {}

        # 4. 소환사 upsert
        account = repo.upsert_riot_account(game_name, tag_line, puuid, region.upper())
        repo.upsert_summoner(
            account.id,
            puuid,  # summonerId 미제공 API 대응: puuid를 고유 식별자로 사용
            region.upper(),
            summoner_data.get("profileIconId"),
            summoner_data.get("summonerLevel"),
        )

        # 5. 최근 매치 ID 조회 후 미수집 매치만 저장
        try:
            match_ids = await riot.get_match_ids_by_puuid(puuid, routing=routing, count=matches_per_summoner)
        except Exception as exc:
            logger.warning("match_ids fetch failed for puuid %s: %s", puuid, exc)
            continue

        for match_id in match_ids:
            if repo.get_match_by_match_id(match_id):
                skipped_matches += 1
                continue
            try:
                raw = await riot.get_match(match_id, routing=routing)
                repo.create_match_from_raw(match_id, raw, region.upper())
                collected_matches += 1
            except Exception as exc:
                logger.warning("match fetch/save failed for %s: %s", match_id, exc)
                continue

        collected_summoners += 1

    # commit은 호출자(run_collection_background)가 담당
    return {
        "summoners": collected_summoners,
        "new_matches": collected_matches,
        "skipped_matches": skipped_matches,
    }
