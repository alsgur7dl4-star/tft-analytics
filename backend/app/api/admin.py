from fastapi import APIRouter, BackgroundTasks

from app.api.deps import AdminUser, DbSession
from app.schemas.admin import (
    BatchJobLogResponse,
    CommonCodeCreate,
    CommonCodeGroupCreate,
    CommonCodeGroupResponse,
    CommonCodeResponse,
    DataSourceResponse,
    JobRunResponse,
    JobTriggerResponse,
)
from app.services.admin_service import AdminService, run_collection_background
from app.services.common_code_service import CommonCodeService

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/jobs/collect-tft-matches", response_model=JobTriggerResponse)
async def collect_tft_matches(
    background_tasks: BackgroundTasks, db: DbSession, _: AdminUser
) -> JobTriggerResponse:
    response = AdminService(db).create_collection_run()
    background_tasks.add_task(run_collection_background, response.job_run_id)
    return response


@router.post("/jobs/recalculate-tft-stats", response_model=JobTriggerResponse)
def recalculate_tft_stats(db: DbSession, _: AdminUser) -> JobTriggerResponse:
    return AdminService(db).trigger_recalculate_stats_job()


@router.get("/jobs/runs", response_model=list[JobRunResponse])
def list_job_runs(db: DbSession, _: AdminUser) -> list[JobRunResponse]:
    return AdminService(db).list_runs()


@router.get("/jobs/runs/{run_id}/logs", response_model=list[BatchJobLogResponse])
def get_job_logs(run_id: int, db: DbSession, _: AdminUser) -> list[BatchJobLogResponse]:
    return AdminService(db).list_run_logs(run_id)


@router.get("/data-sources", response_model=list[DataSourceResponse])
def list_data_sources(db: DbSession, _: AdminUser) -> list[DataSourceResponse]:
    return AdminService(db).list_data_sources()


@router.get("/codes/groups", response_model=list[CommonCodeGroupResponse])
def list_code_groups(db: DbSession, _: AdminUser) -> list[CommonCodeGroupResponse]:
    return CommonCodeService(db).list_groups()


@router.post("/codes/groups", response_model=CommonCodeGroupResponse, status_code=201)
def create_code_group(body: CommonCodeGroupCreate, db: DbSession, _: AdminUser) -> CommonCodeGroupResponse:
    return CommonCodeService(db).create_group(body.group_key, body.group_name, body.description)


@router.delete("/codes/groups/{group_key}", status_code=204)
def delete_code_group(group_key: str, db: DbSession, _: AdminUser) -> None:
    CommonCodeService(db).delete_group(group_key)


@router.post("/codes/groups/{group_key}/codes", response_model=CommonCodeResponse, status_code=201)
def add_code(group_key: str, body: CommonCodeCreate, db: DbSession, _: AdminUser) -> CommonCodeResponse:
    return CommonCodeService(db).add_code(group_key, body.code, body.label, body.sort_order, body.meta_json)


@router.delete("/codes/{code_id}", status_code=204)
def delete_code(code_id: int, db: DbSession, _: AdminUser) -> None:
    CommonCodeService(db).delete_code(code_id)
