from sqlalchemy.orm import Session


def recalculate_tft_stats(_: Session) -> dict[str, str]:
    return {"status": "TODO", "message": "Aggregation scaffold is ready; implement live comp grouping after data collection."}

