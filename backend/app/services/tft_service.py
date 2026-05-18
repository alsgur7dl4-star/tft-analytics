from fastapi import status
from sqlalchemy.orm import Session

from app.clients.riot_tft_client import RiotTftClient
from app.core import error_codes
from app.core.exceptions import AppException
from app.repositories.tft_repository import TftRepository
from app.schemas.tft import MatchParticipantResponse, MatchSummaryResponse, RiotAccountResponse, SummonerSummaryResponse


class TftService:
    def __init__(self, db: Session, riot_client: RiotTftClient | None = None):
        self.db = db
        self.repo = TftRepository(db)
        self.riot_client = riot_client or RiotTftClient()

    async def search_account(self, game_name: str, tag_line: str, region: str) -> RiotAccountResponse:
        riot_account = await self.riot_client.get_account_by_riot_id(game_name, tag_line)
        account = self.repo.upsert_riot_account(
            riot_account["gameName"],
            riot_account["tagLine"],
            riot_account["puuid"],
            region,
        )
        summoner = await self.riot_client.get_summoner_by_puuid(account.puuid, region.lower())
        self.repo.upsert_summoner(
            account.id,
            summoner["id"],
            region,
            summoner.get("profileIconId"),
            summoner.get("summonerLevel"),
        )
        self.db.commit()
        return RiotAccountResponse.model_validate(account)

    async def get_summoner_summary(self, puuid: str) -> SummonerSummaryResponse:
        account = self.repo.get_account_by_puuid(puuid)
        if not account:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, "Riot account is not collected yet", status.HTTP_404_NOT_FOUND)
        matches = self.repo.list_matches_for_puuid(puuid)
        placements = [
            participant.placement
            for match in matches
            for participant in match.participants
            if participant.puuid == puuid
        ]
        avg = sum(placements) / len(placements) if placements else None
        top4 = sum(1 for placement in placements if placement <= 4) / len(placements) if placements else None
        first = sum(1 for placement in placements if placement == 1) / len(placements) if placements else None
        return SummonerSummaryResponse(
            puuid=account.puuid,
            game_name=account.game_name,
            tag_line=account.tag_line,
            region=account.region,
            recent_matches=len(matches),
            avg_placement=avg,
            top4_rate=top4,
            first_rate=first,
        )

    async def collect_recent_matches(self, puuid: str, count: int = 20, region: str = "KR") -> list[MatchSummaryResponse]:
        match_ids = await self.riot_client.get_match_ids_by_puuid(puuid, count=count)
        for match_id in match_ids:
            if self.repo.get_match_by_match_id(match_id):
                continue
            raw = await self.riot_client.get_match(match_id)
            self.repo.create_match_from_raw(match_id, raw, region)
        self.db.commit()
        return [self._match_to_response(match) for match in self.repo.list_matches_for_puuid(puuid, limit=count)]

    async def get_match(self, match_id: str) -> MatchSummaryResponse:
        match = self.repo.get_match_by_match_id(match_id)
        if not match:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, "Match is not collected yet", status.HTTP_404_NOT_FOUND)
        return self._match_to_response(match)

    def _match_to_response(self, match) -> MatchSummaryResponse:
        return MatchSummaryResponse(
            match_id=match.match_id,
            game_version=match.game_version,
            game_datetime=match.game_datetime,
            queue_id=match.queue_id,
            participants=[
                MatchParticipantResponse(
                    puuid=participant.puuid,
                    placement=participant.placement,
                    level=participant.level,
                    traits=participant.traits_json or [],
                    units=participant.units_json or [],
                    augments=participant.augments_json or [],
                )
                for participant in match.participants
            ],
        )

