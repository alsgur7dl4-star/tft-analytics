from sqlalchemy.orm import Session

from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.stats_repository import StatsRepository
from app.recommenders.artifact_recommender import recommend_from_artifacts
from app.recommenders.early_game_recommender import recommend_from_early_units
from app.schemas.recommendation import (
    ArtifactRecommendationRequest,
    EarlyGameRecommendationRequest,
    RecommendationResult,
)


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.stats = StatsRepository(db)
        self.logs = RecommendationRepository(db)

    def recommend_early_game(self, user_id: int, data: EarlyGameRecommendationRequest) -> list[RecommendationResult]:
        results = recommend_from_early_units(self.stats.list_latest_comp_stats(limit=100), data.units, data.items, data.augments)
        self.logs.create_log(
            user_id,
            [result.model_dump() for result in results],
            input_units=data.units,
            input_items=data.items,
            input_augments=data.augments,
        )
        self.db.commit()
        return results

    def recommend_artifacts(self, user_id: int, data: ArtifactRecommendationRequest) -> list[RecommendationResult]:
        results = recommend_from_artifacts(self.stats.list_latest_comp_stats(limit=100), data.items)
        self.logs.create_log(user_id, [result.model_dump() for result in results], input_items=data.items)
        self.db.commit()
        return results

