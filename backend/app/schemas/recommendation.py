from typing import Any

from pydantic import BaseModel, Field, field_validator


class EarlyGameRecommendationRequest(BaseModel):
    units: list[str] = Field(min_length=3, max_length=8)
    items: list[str] = Field(default_factory=list, max_length=8)
    augments: list[str] = Field(default_factory=list, max_length=8)


class ArtifactRecommendationRequest(BaseModel):
    items: list[str] = Field(min_length=1, max_length=4)

    @field_validator("items")
    @classmethod
    def unique_items(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(value))


class RecommendationResult(BaseModel):
    rank: int
    comp_id: int
    comp_name: str
    score: float
    tier_label: str | None = None
    core_units: list[Any] = Field(default_factory=list)
    final_comp: list[Any] = Field(default_factory=list)
    matching_rate: float | None = None
    synergy_score: float | None = None
    avg_placement: float | None = None
    top4_rate: float | None = None
    first_rate: float | None = None
    pick_rate: float | None = None
    difficulty: str = "MEDIUM"
    reason: str

