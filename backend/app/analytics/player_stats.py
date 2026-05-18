def summarize_placements(placements: list[int]) -> dict[str, float | int | None]:
    if not placements:
        return {"games": 0, "avg_placement": None, "top4_rate": None, "first_rate": None}
    games = len(placements)
    return {
        "games": games,
        "avg_placement": round(sum(placements) / games, 2),
        "top4_rate": round(sum(1 for placement in placements if placement <= 4) / games, 4),
        "first_rate": round(sum(1 for placement in placements if placement == 1) / games, 4),
    }

