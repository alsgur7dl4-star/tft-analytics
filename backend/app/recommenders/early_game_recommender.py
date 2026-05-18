from app.schemas.recommendation import RecommendationResult


def recommend_from_early_units(
    comp_rows: list[tuple],
    owned_units: list[str],
    items: list[str],
    augments: list[str],
) -> list[RecommendationResult]:
    owned = {unit.lower() for unit in owned_units}
    owned_items = {item.lower() for item in items}
    owned_augments = {augment.lower() for augment in augments}
    results: list[RecommendationResult] = []
    for stat, comp in comp_rows:
        core_units = comp.core_units_json or []
        core_items = comp.core_items_json or []
        core_traits = comp.core_traits_json or []
        core_unit_names = {str(unit).lower() for unit in core_units}
        core_item_names = {str(item).lower() for item in core_items}
        unit_match = len(owned & core_unit_names) / max(len(core_unit_names), 1)
        core_match = 1.0 if owned & core_unit_names else 0.0
        item_match = len(owned_items & core_item_names) / max(len(owned_items), 1) if owned_items else 0.0
        augment_match = 0.2 if owned_augments and core_traits else 0.0
        score = unit_match * 0.35 + core_match * 0.25 + item_match * 0.15 + augment_match * 0.10 + stat.score * 0.15
        results.append(
            RecommendationResult(
                rank=0,
                comp_id=comp.id,
                comp_name=comp.comp_name,
                score=round(score, 4),
                tier_label=stat.tier_label,
                core_units=core_units,
                final_comp=core_units,
                matching_rate=round(unit_match, 4),
                avg_placement=stat.avg_placement,
                top4_rate=stat.top4_rate,
                first_rate=stat.first_rate,
                pick_rate=stat.pick_rate,
                difficulty="MEDIUM" if stat.pick_rate >= 0.03 else "HIGH",
                reason="보유 기물과 핵심 기물이 겹치고 최근 메타 점수가 반영된 추천입니다.",
            )
        )
    results.sort(key=lambda result: result.score, reverse=True)
    for index, result in enumerate(results[:10], start=1):
        result.rank = index
    return results[:10]

