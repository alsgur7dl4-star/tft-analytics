from sqlalchemy.orm import Session

from app.models.tft import TftRecommendationLog


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(
        self,
        user_id: int,
        result: list[dict],
        input_units: list[str] | None = None,
        input_items: list[str] | None = None,
        input_augments: list[str] | None = None,
        input_gods: list[str] | None = None,
    ) -> TftRecommendationLog:
        log = TftRecommendationLog(
            user_id=user_id,
            input_units_json=input_units,
            input_items_json=input_items,
            input_augments_json=input_augments,
            input_gods_json=input_gods,
            recommendation_result_json=result,
        )
        self.db.add(log)
        self.db.flush()
        return log

