from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tft import TftComp, TftCompStatsDaily, TftItem, TftUnitStatsDaily


class StatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_latest_comp_stats(self, limit: int = 50) -> list[tuple[TftCompStatsDaily, TftComp]]:
        latest_date = self.db.scalar(select(TftCompStatsDaily.stat_date).order_by(TftCompStatsDaily.stat_date.desc()).limit(1))
        if not latest_date:
            return []
        return list(
            self.db.execute(
                select(TftCompStatsDaily, TftComp)
                .join(TftComp)
                .where(TftCompStatsDaily.stat_date == latest_date)
                .order_by(TftCompStatsDaily.score.desc())
                .limit(limit)
            )
        )

    def get_comp_with_latest_stats(self, comp_id: int) -> tuple[TftCompStatsDaily, TftComp] | None:
        return self.db.execute(
            select(TftCompStatsDaily, TftComp)
            .join(TftComp)
            .where(TftComp.id == comp_id)
            .order_by(TftCompStatsDaily.stat_date.desc())
            .limit(1)
        ).one_or_none()

    def list_latest_unit_stats(self, limit: int = 50) -> list[TftUnitStatsDaily]:
        latest_date = self.db.scalar(select(TftUnitStatsDaily.stat_date).order_by(TftUnitStatsDaily.stat_date.desc()).limit(1))
        if not latest_date:
            return []
        return list(
            self.db.scalars(
                select(TftUnitStatsDaily)
                .where(TftUnitStatsDaily.stat_date == latest_date)
                .order_by(TftUnitStatsDaily.games.desc())
                .limit(limit)
            )
        )

    def list_items(self, limit: int = 200) -> list[TftItem]:
        return list(self.db.scalars(select(TftItem).order_by(TftItem.item_name.asc()).limit(limit)))

