import asyncio
from typing import Any

import httpx
from fastapi import status

from app.core import error_codes
from app.core.config import settings
from app.core.exceptions import AppException


class RiotTftClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.riot_api_key

    def _require_key(self) -> None:
        if not self.api_key:
            raise AppException(
                error_codes.RIOT_API_ERROR,
                "Riot API key is not configured",
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    async def _request(self, url: str, params: dict[str, Any] | None = None) -> Any:
        self._require_key()
        headers = {"X-Riot-Token": self.api_key}
        timeout = httpx.Timeout(10.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            for attempt in range(3):
                response = await client.get(url, headers=headers, params=params)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "1"))
                    await asyncio.sleep(min(retry_after, 10))
                    continue
                if response.status_code >= 400:
                    raise AppException(
                        error_codes.RIOT_API_ERROR,
                        "Riot API request failed",
                        status.HTTP_502_BAD_GATEWAY,
                        {"status_code": response.status_code},
                    )
                return response.json()
            raise AppException(error_codes.RIOT_API_ERROR, "Riot API rate limit retry exhausted", status.HTTP_429_TOO_MANY_REQUESTS)

    async def get_account_by_riot_id(self, game_name: str, tag_line: str, routing: str | None = None) -> dict[str, Any]:
        routing = routing or settings.riot_default_routing
        url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return await self._request(url)

    async def get_summoner_by_puuid(self, puuid: str, region: str | None = None) -> dict[str, Any]:
        region = region or settings.riot_default_region
        url = f"https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
        return await self._request(url)

    async def get_match_ids_by_puuid(
        self, puuid: str, routing: str | None = None, start: int = 0, count: int = 20
    ) -> list[str]:
        routing = routing or settings.riot_default_routing
        url = f"https://{routing}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
        return await self._request(url, {"start": start, "count": count})

    async def get_match(self, match_id: str, routing: str | None = None) -> dict[str, Any]:
        routing = routing or settings.riot_default_routing
        url = f"https://{routing}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        return await self._request(url)

