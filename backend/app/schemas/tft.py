from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RiotAccountResponse(BaseModel):
    game_name: str
    tag_line: str
    puuid: str
    region: str

    model_config = {"from_attributes": True}


class SummonerSummaryResponse(BaseModel):
    puuid: str
    game_name: str
    tag_line: str
    region: str
    recent_matches: int = 0
    avg_placement: float | None = None
    top4_rate: float | None = None
    first_rate: float | None = None


class MatchParticipantResponse(BaseModel):
    puuid: str
    placement: int
    level: int | None = None
    traits: list[Any] = Field(default_factory=list)
    units: list[Any] = Field(default_factory=list)
    augments: list[Any] = Field(default_factory=list)


class MatchSummaryResponse(BaseModel):
    match_id: str
    game_version: str | None = None
    game_datetime: datetime | None = None
    queue_id: int | None = None
    participants: list[MatchParticipantResponse] = Field(default_factory=list)


class CompStatsResponse(BaseModel):
    comp_id: int
    comp_name: str
    tier_label: str
    score: float
    games: int
    avg_placement: float
    top4_rate: float
    first_rate: float
    pick_rate: float
    core_units: list[Any] = Field(default_factory=list)
    core_traits: list[Any] = Field(default_factory=list)
    core_items: list[Any] = Field(default_factory=list)


class UnitStatsResponse(BaseModel):
    unit_key: str
    unit_name: str | None = None
    games: int
    avg_placement: float
    top4_rate: float
    first_rate: float
    pick_rate: float

