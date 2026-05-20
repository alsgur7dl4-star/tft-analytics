from app.schemas.recommendation import RecommendationResult

_DIFFICULTY_BY_PICK_RATE = [
    (0.05, "EASY"),
    (0.02, "MEDIUM"),
]


def _difficulty(pick_rate: float) -> str:
    for threshold, label in _DIFFICULTY_BY_PICK_RATE:
        if pick_rate >= threshold:
            return label
    return "HIGH"


def recommend_from_early_units(
    comp_rows: list[tuple],
    owned_units: list[str],
    items: list[str],
    augments: list[str],
    gods: list[str] | None = None,
) -> list[RecommendationResult]:
    owned = {unit.lower() for unit in owned_units}
    owned_items = {item.lower() for item in items}
    owned_augments = {augment.lower() for augment in augments}
    owned_gods = {god.lower() for god in (gods or [])}
    results: list[RecommendationResult] = []
    for stat, comp in comp_rows:
        core_units = comp.core_units_json or []
        core_items = comp.core_items_json or []
        core_traits = comp.core_traits_json or []
        preferred_gods = [str(g).lower() for g in (comp.preferred_gods_json or [])]
        preferred_gods_set = set(preferred_gods)

        core_unit_names = {str(unit).lower() for unit in core_units}
        core_item_names = {str(item).lower() for item in core_items}

        unit_match = len(owned & core_unit_names) / max(len(core_unit_names), 1)
        core_match = 1.0 if owned & core_unit_names else 0.0
        item_match = len(owned_items & core_item_names) / max(len(owned_items), 1) if owned_items else 0.0
        augment_match = 1.0 if owned_augments and core_traits else 0.0

        if preferred_gods_set and owned_gods:
            god_match_score = 1.0 if owned_gods & preferred_gods_set else 0.0
        elif not preferred_gods_set:
            god_match_score = 0.5
        else:
            god_match_score = 0.0

        god_matched = bool(preferred_gods_set and owned_gods and owned_gods & preferred_gods_set)

        score = (
            unit_match * 0.30
            + core_match * 0.20
            + item_match * 0.15
            + god_match_score * 0.15
            + augment_match * 0.05
            + stat.score * 0.15
        )

        reason_parts: list[str] = []
        if unit_match >= 0.5:
            reason_parts.append("보유 기물 다수 일치")
        if core_match:
            reason_parts.append("코어 기물 보유")
        if item_match >= 0.3:
            reason_parts.append("아이템 적합")
        if god_matched:
            reason_parts.append("신 선택 일치")
        reason = "·".join(reason_parts) + "하여 추천" if reason_parts else "메타 점수 기반 추천"

        results.append(
            RecommendationResult(
                rank=0,
                comp_id=comp.id,
                comp_name=comp.comp_name,
                score=round(score, 4),
                tier_label=stat.tier_label,
                core_units=core_units,
                final_comp=core_units,
                preferred_gods=list(comp.preferred_gods_json or []),
                god_match=god_matched,
                matching_rate=round(unit_match, 4),
                avg_placement=stat.avg_placement,
                top4_rate=stat.top4_rate,
                first_rate=stat.first_rate,
                pick_rate=stat.pick_rate,
                difficulty=_difficulty(stat.pick_rate),
                reason=reason,
            )
        )
    results.sort(key=lambda result: result.score, reverse=True)
    for index, result in enumerate(results[:10], start=1):
        result.rank = index
    return results[:10]
