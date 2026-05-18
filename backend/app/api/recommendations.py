from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.recommendation import ArtifactRecommendationRequest, EarlyGameRecommendationRequest, RecommendationResult
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/tft/recommendations", tags=["recommendations"])


@router.post("/early-game", response_model=list[RecommendationResult])
def recommend_early_game(
    payload: EarlyGameRecommendationRequest,
    db: DbSession,
    current_user: CurrentUser,
) -> list[RecommendationResult]:
    return RecommendationService(db).recommend_early_game(current_user.id, payload)


@router.post("/artifacts", response_model=list[RecommendationResult])
def recommend_artifacts(
    payload: ArtifactRecommendationRequest,
    db: DbSession,
    current_user: CurrentUser,
) -> list[RecommendationResult]:
    return RecommendationService(db).recommend_artifacts(current_user.id, payload)

