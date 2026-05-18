from sqlalchemy.orm import Session

from app.jobs.tft_stats_aggregator import recalculate_tft_stats
from app.repositories.job_repository import JobRepository
from app.schemas.admin import DataSourceResponse, JobRunResponse, JobTriggerResponse


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.jobs = JobRepository(db)

    def trigger_collection_job(self) -> JobTriggerResponse:
        run = self.jobs.create_run("collect-tft-matches")
        self.jobs.finish_run(run, "SUCCESS", "Collection job scaffold created. Wire target PUUIDs in the next iteration.")
        self.db.commit()
        return JobTriggerResponse(job_run_id=run.id, status=run.status, message=run.message or "")

    def trigger_recalculate_stats_job(self) -> JobTriggerResponse:
        run = self.jobs.create_run("recalculate-tft-stats")
        result = recalculate_tft_stats(self.db)
        self.jobs.finish_run(run, "SUCCESS", result["message"])
        self.db.commit()
        return JobTriggerResponse(job_run_id=run.id, status=run.status, message=run.message or "")

    def list_runs(self) -> list[JobRunResponse]:
        return [JobRunResponse.model_validate(run) for run in self.jobs.list_runs()]

    def list_data_sources(self) -> list[DataSourceResponse]:
        return [DataSourceResponse.model_validate(source) for source in self.jobs.list_data_sources()]

