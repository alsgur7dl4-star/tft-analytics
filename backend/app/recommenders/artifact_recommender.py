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

        matched = selected & core_item_names
        reason_parts: list[str] = []
        if matched:
            reason_parts.append(f"아이템 {len(matched)}개 일치")
        if stat.tier_label in ("S", "A"):
            reason_parts.append(f"{stat.tier_label}티어 덱")
        if reliability >= 0.5:
            reason_parts.append("충분한 표본")
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
                synergy_score=round(synergy, 4),
                avg_placement=stat.avg_placement,
                top4_rate=stat.top4_rate,
                first_rate=stat.first_rate,
                pick_rate=stat.pick_rate,
                reason=reason,
            )
        )
    results.sort(key=lambda result: result.score, reverse=True)
    for index, result in enumerate(results[:10], start=1):
        result.rank = index
    return results[:10]

