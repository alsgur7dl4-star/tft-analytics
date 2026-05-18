from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.common import BatchJobRun, DataSource


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_run(self, job_name: str, meta_json: dict | None = None) -> BatchJobRun:
        run = BatchJobRun(job_name=job_name, status="RUNNING", meta_json=meta_json)
        self.db.add(run)
        self.db.flush()
        return run

    def finish_run(self, run: BatchJobRun, status: str, message: str | None = None) -> BatchJobRun:
        run.status = status
        run.message = message
        run.finished_at = datetime.now(timezone.utc)
        self.db.add(run)
        self.db.flush()
        return run

    def list_runs(self, limit: int = 50) -> list[BatchJobRun]:
        return list(self.db.scalars(select(BatchJobRun).order_by(BatchJobRun.started_at.desc()).limit(limit)))

    def list_data_sources(self) -> list[DataSource]:
        return list(self.db.scalars(select(DataSource).order_by(DataSource.source_key.asc())))

