from app.schemas.recommendation import RecommendationResult


def recommend_from_artifacts(comp_rows: list[tuple], items: list[str]) -> list[RecommendationResult]:
    selected = {item.lower() for item in items}
    results: list[RecommendationResult] = []
    for stat, comp in comp_rows:
        core_items = comp.core_items_json or []
        core_units = comp.core_units_json or []
        core_item_names = {str(item).lower() for item in core_items}
        synergy = len(selected & core_item_names) / max(len(selected), 1)
        carry_item_score = 1.0 if selected & core_item_names else 0.0
        reliability = min(stat.games / 200.0, 1.0)
        score = synergy * 0.45 + carry_item_score * 0.25 + stat.score * 0.20 + reliability * 0.10
        results.append(
            RecommendationResult(
                rank=0,
                comp_id=comp.id,
                comp_name=comp.comp_name,
                score=round(score, 4),
                tier_label=stat.tier_label,
                core_units=core_units,
                final_comp=core_units,
                synergy_score=round(synergy, 4),
                avg_placement=stat.avg_placement,
                top4_rate=stat.top4_rate,
                first_rate=stat.first_rate,
                pick_rate=stat.pick_rate,
                reason="선택한 유물/아이템과 핵심 아이템 룰, 메타 점수, 표본 안정성을 함께 반영했습니다.",
            )
        )
    results.sort(key=lambda result: result.score, reverse=True)
    for index, result in enumerate(results[:10], start=1):
        result.rank = index
    return results[:10]

