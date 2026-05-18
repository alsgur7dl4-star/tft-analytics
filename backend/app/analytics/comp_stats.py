def normalized_avg_placement_score(avg_placement: float) -> float:
    return max(0.0, min(1.0, (8.0 - avg_placement) / 7.0))


def calculate_comp_score(
    top4_rate: float,
    first_rate: float,
    pick_rate: float,
    avg_placement: float,
    max_pick_rate: float,
    sample_count: int,
    min_sample_count: int = 30,
) -> float:
    if sample_count < min_sample_count:
        return 0.0
    normalized_pick_rate = pick_rate / max(max_pick_rate, 0.0001)
    score = (
        top4_rate * 0.35
        + first_rate * 0.25
        + min(normalized_pick_rate, 1.0) * 0.15
        + normalized_avg_placement_score(avg_placement) * 0.25
    )
    return round(score, 4)


def assign_tier_label(rank_ratio: float) -> str:
    if rank_ratio <= 0.10:
        return "S"
    if rank_ratio <= 0.25:
        return "A"
    if rank_ratio <= 0.50:
        return "B"
    if rank_ratio <= 0.75:
        return "C"
    return "D"

