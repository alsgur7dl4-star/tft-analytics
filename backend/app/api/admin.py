from fastapi import APIRouter

from app.api.deps import AdminUser, DbSession
from app.schemas.admin import DataSourceResponse, JobRunResponse, JobTriggerResponse
from app.services.admin_service import AdminService

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/jobs/collect-tft-matches", response_model=JobTriggerResponse)
def collect_tft_matches(db: DbSession, _: AdminUser) -> JobTriggerResponse:
    return AdminService(db).trigger_collection_job()


@router.post("/jobs/recalculate-tft-stats", response_model=JobTriggerResponse)
def recalculate_tft_stats(db: DbSession, _: AdminUser) -> JobTriggerResponse:
    return AdminService(db).trigger_recalculate_stats_job()


@router.get("/jobs/runs", response_model=list[JobRunResponse])
def list_job_runs(db: DbSession, _: AdminUser) -> list[JobRunResponse]:
    return AdminService(db).list_runs()


@router.get("/data-sources", response_model=list[DataSourceResponse])
def list_data_sources(db: DbSession, _: AdminUser) -> list[DataSourceResponse]:
    return AdminService(db).list_data_sources()

