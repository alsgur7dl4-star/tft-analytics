from sqlalchemy.orm import Session

from app.services.tft_service import TftService


async def collect_matches_for_puuid(db: Session, puuid: str, count: int = 20, region: str = "KR") -> int:
    matches = await TftService(db).collect_recent_matches(puuid, count=count, region=region)
    return len(matches)

