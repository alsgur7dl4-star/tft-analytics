from fastapi import status
from sqlalchemy.orm import Session

from app.core import error_codes
from app.core.exceptions import AppException
from app.repositories.stats_repository import StatsRepository
from app.schemas.tft import ChampionResponse, CompStatsResponse, GodResponse, UnitStatsResponse


class MetaService:
    def __init__(self, db: Session):
        self.stats = StatsRepository(db)

    def list_comps(self) -> list[CompStatsResponse]:
        return [self._comp_stats_to_response(stat, comp) for stat, comp in self.stats.list_latest_comp_stats()]

    def get_comp(self, comp_id: int) -> CompStatsResponse:
        row = self.stats.get_comp_with_latest_stats(comp_id)
        if not row:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, "Composition was not found", status.HTTP_404_NOT_FOUND)
        stat, comp = row
        return self._comp_stats_to_response(stat, comp)

    def list_units(self) -> list[UnitStatsResponse]:
        return [UnitStatsResponse.model_validate(unit, from_attributes=True) for unit in self.stats.list_latest_unit_stats()]

    def list_items(self) -> list[dict]:
        return [
            {
                "item_key": item.item_key,
                "item_name": item.item_name,
                "item_type": item.item_type,
                "set_name": item.set_name,
                "is_artifact": bool(item.is_artifact),
            }
            for item in self.stats.list_items()
        ]

    def list_augments(self) -> list[dict]:
        return [{"augment_key": key} for key in self.stats.list_augment_keys()]

    def list_gods(self, set_name: str | None = None) -> list[GodResponse]:
        return [GodResponse.model_validate(god, from_attributes=True) for god in self.stats.list_gods(set_name)]

    def list_champions(self) -> list[ChampionResponse]:
        rows = self.stats.list_unit_keys()
        return [ChampionResponse(unit_key=r["unit_key"], unit_name=r["unit_name"]) for r in rows]

    def _comp_stats_to_response(self, stat, comp) -> CompStatsResponse:
        return CompStatsResponse(
            comp_id=comp.id,
            comp_name=comp.comp_name,
            tier_label=stat.tier_label,
            score=stat.score,
            games=stat.games,
            avg_placement=stat.avg_placement,
            top4_rate=stat.top4_rate,
            first_rate=stat.first_rate,
            pick_rate=stat.pick_rate,
            core_units=comp.core_units_json or [],
            core_traits=comp.core_traits_json or [],
            core_items=comp.core_items_json or [],
        )

