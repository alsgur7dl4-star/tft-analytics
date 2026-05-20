from sqlalchemy import distinct, select
from sqlalchemy.orm import Session

from app.models.tft import TftAugment, TftComp, TftCompStatsDaily, TftItem, TftStaticGod, TftUnit, TftUnitStatsDaily


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

    def list_gods(self, set_name: str | None = None) -> list[TftStaticGod]:
        q = select(TftStaticGod)
        if set_name:
            q = q.where(TftStaticGod.set_name == set_name)
        return list(self.db.scalars(q.order_by(TftStaticGod.sort_order.asc(), TftStaticGod.god_name.asc())))

    def list_augment_keys(self, limit: int = 300) -> list[str]:
        rows = self.db.execute(
            select(TftAugment.augment_key)
            .where(TftAugment.augment_key != "")
            .distinct(TftAugment.augment_key)
            .order_by(TftAugment.augment_key.asc())
            .limit(limit)
        ).all()
        return [row[0] for row in rows]

    def list_unit_keys(self, limit: int = 200) -> list[dict]:
        rows = self.db.execute(
            select(TftUnit.character_id, TftUnit.name)
            .where(TftUnit.character_id != "")
            .distinct(TftUnit.character_id)
            .order_by(TftUnit.character_id.asc())
            .limit(limit)
        ).all()
        return [{"unit_key": char_id, "unit_name": name} for char_id, name in rows]

