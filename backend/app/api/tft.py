from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, DbSession
from app.schemas.tft import CompStatsResponse, MatchSummaryResponse, RiotAccountResponse, SummonerSummaryResponse, UnitStatsResponse
from app.services.meta_service import MetaService
from app.services.tft_service import TftService

router = APIRouter(prefix="/api/tft", tags=["tft"])


@router.get("/accounts/search", response_model=RiotAccountResponse)
async def search_account(
    db: DbSession,
    _: CurrentUser,
    game_name: str = Query(min_length=1),
    tag_line: str = Query(min_length=1),
    region: str = "KR",
) -> RiotAccountResponse:
    return await TftService(db).search_account(game_name, tag_line, region)


@router.get("/summoners/{puuid}", response_model=SummonerSummaryResponse)
async def get_summoner(puuid: str, db: DbSession, _: CurrentUser) -> SummonerSummaryResponse:
    return await TftService(db).get_summoner_summary(puuid)


@router.get("/summoners/{puuid}/matches", response_model=list[MatchSummaryResponse])
async def get_summoner_matches(puuid: str, db: DbSession, _: CurrentUser, count: int = 20) -> list[MatchSummaryResponse]:
    return await TftService(db).collect_recent_matches(puuid, count=count)


@router.get("/matches/{match_id}", response_model=MatchSummaryResponse)
async def get_match(match_id: str, db: DbSession, _: CurrentUser) -> MatchSummaryResponse:
    return await TftService(db).get_match(match_id)


@router.get("/meta/comps", response_model=list[CompStatsResponse])
def list_comps(db: DbSession, _: CurrentUser) -> list[CompStatsResponse]:
    return MetaService(db).list_comps()


@router.get("/meta/comps/{comp_id}", response_model=CompStatsResponse)
def get_comp(comp_id: int, db: DbSession, _: CurrentUser) -> CompStatsResponse:
    return MetaService(db).get_comp(comp_id)


@router.get("/meta/units", response_model=list[UnitStatsResponse])
def list_units(db: DbSession, _: CurrentUser) -> list[UnitStatsResponse]:
    return MetaService(db).list_units()


@router.get("/meta/items")
def list_items(db: DbSession, _: CurrentUser) -> list[dict]:
    return MetaService(db).list_items()


@router.get("/meta/augments")
def list_augments(db: DbSession, _: CurrentUser) -> list[dict]:
    return MetaService(db).list_augments()

