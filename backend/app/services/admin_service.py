from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.jobs.tft_stats_aggregator import recalculate_tft_stats
from app.repositories.job_repository import JobRepository
from app.schemas.admin import BatchJobLogResponse, DataSourceResponse, JobRunResponse, JobTriggerResponse


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.jobs = JobRepository(db)

    def create_collection_run(self) -> JobTriggerResponse:
        """배치 잡 실행 레코드 생성 후 즉시 반환 (실제 수집은 백그라운드에서 실행)."""
        run = self.jobs.create_run("collect-tft-matches")
        self.jobs.add_log(run, "매치 수집 잡 예약됨", step="QUEUED")
        self.db.commit()
        return JobTriggerResponse(job_run_id=run.id, status="RUNNING", message="백그라운드 수집 시작됨")

    def trigger_recalculate_stats_job(self) -> JobTriggerResponse:
        run = self.jobs.create_run("recalculate-tft-stats")
        try:
            self.jobs.add_log(run, "통계 재계산 시작", step="START")
            result = recalculate_tft_stats(self.db)
            self.jobs.add_log(run, result["message"], step="COMPLETE")
            self.jobs.finish_run(run, "SUCCESS", result["message"])
        except Exception as exc:
            self.jobs.add_log(run, str(exc), step="ERROR", log_level="ERROR")
            self.jobs.finish_run(run, "FAILED", str(exc))
        self.db.commit()
        return JobTriggerResponse(job_run_id=run.id, status=run.status, message=run.message or "")

    def list_runs(self) -> list[JobRunResponse]:
        return [JobRunResponse.model_validate(run) for run in self.jobs.list_runs()]

    def list_run_logs(self, run_id: int) -> list[BatchJobLogResponse]:
        return [BatchJobLogResponse.model_validate(log) for log in self.jobs.list_logs(run_id)]

    def list_data_sources(self) -> list[DataSourceResponse]:
        return [DataSourceResponse.model_validate(source) for source in self.jobs.list_data_sources()]


async def run_collection_background(run_id: int) -> None:
    """BackgroundTask로 실행: 독립 DB 세션에서 고티어 매치 수집 후 잡 상태 업데이트."""
    from app.jobs.tft_match_collector import collect_top_elo_matches
    from app.models.common import BatchJobRun

    with SessionLocal() as db:
        jobs = JobRepository(db)
        run = db.get(BatchJobRun, run_id)
        if not run:
            return
        try:
            jobs.add_log(run, "챌린저/그랜드마스터 소환사 목록 조회 시작", step="FETCH_LEAGUE")
            db.commit()

            result = await collect_top_elo_matches(db, max_summoners=30, matches_per_summoner=10)
            db.commit()

            jobs.add_log(
                run,
                f"소환사 {result['summoners']}명 / 신규 매치 {result['new_matches']}개 / 중복 스킵 {result['skipped_matches']}개",
                step="COMPLETE",
                meta_json=result,
            )
            jobs.finish_run(
                run,
                "SUCCESS",
                f"신규 매치 {result['new_matches']}개 수집 완료",
            )
        except Exception as exc:
            jobs.add_log(run, str(exc), step="ERROR", log_level="ERROR")
            jobs.finish_run(run, "FAILED", str(exc))
        db.commit()
