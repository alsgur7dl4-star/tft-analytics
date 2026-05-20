from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.common import BatchJobLog, BatchJobRun, DataSource


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

    def add_log(
        self,
        run: BatchJobRun,
        message: str,
        step: str | None = None,
        log_level: str = "INFO",
        meta_json: dict | None = None,
    ) -> BatchJobLog:
        log = BatchJobLog(
            job_run_id=run.id,
            log_level=log_level,
            step=step,
            message=message,
            meta_json=meta_json,
        )
        self.db.add(log)
        self.db.flush()
        return log

    def list_runs(self, limit: int = 50) -> list[BatchJobRun]:
        return list(self.db.scalars(select(BatchJobRun).order_by(BatchJobRun.started_at.desc()).limit(limit)))

    def list_logs(self, run_id: int) -> list[BatchJobLog]:
        return list(
            self.db.scalars(
                select(BatchJobLog)
                .where(BatchJobLog.job_run_id == run_id)
                .order_by(BatchJobLog.created_at.asc())
            )
        )

    def list_data_sources(self) -> list[DataSource]:
        return list(self.db.scalars(select(DataSource).order_by(DataSource.source_key.asc())))

