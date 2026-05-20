# TFT Analytics Handoff

## Current State

- Project scaffold initialized for a standalone TFT analytics service.
- Dedicated PostgreSQL Docker resources are running and separated from any `jobfit-ai` resources.
- Backend and frontend source trees are present, with authentication gates for primary product routes.

## Database

- Container: `tft_analytics_postgres`
- Database: `tft_analytics_db`
- User: `tft_analytics_user`
- Volume: `tft_analytics_postgres_data`
- Host port: `5433`
- Status: Docker container is running and healthy.

Initial Alembic migration creates:

- `users`
- `refresh_tokens`
- `common_code_groups`
- `common_codes`
- `data_sources`
- `batch_job_runs`
- `riot_accounts`
- `tft_summoners`
- `tft_league_entries`
- `tft_matches`
- `tft_match_participants`
- `tft_units`
- `tft_traits`
- `tft_augments`
- `tft_items`
- `tft_comps`
- `tft_comp_stats_daily`
- `tft_unit_stats_daily`
- `tft_recommendation_logs`

## APIs

- Auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`, `/api/auth/logout`, `/api/auth/me`
- TFT lookup: `/api/tft/accounts/search`, `/api/tft/summoners/{puuid}`, `/api/tft/summoners/{puuid}/matches`, `/api/tft/matches/{match_id}`
- Meta: `/api/tft/meta/comps`, `/api/tft/meta/comps/{comp_id}`, `/api/tft/meta/units`, `/api/tft/meta/items`, `/api/tft/meta/augments`
- Recommendations: `/api/tft/recommendations/early-game`, `/api/tft/recommendations/artifacts`
- Admin: `/api/admin/jobs/collect-tft-matches`, `/api/admin/jobs/recalculate-tft-stats`, `/api/admin/jobs/runs`, `/api/admin/data-sources`

## Recent Verification

- `python -m compileall backend` passed on 2026-05-18.
- Local backend virtual environment was created at `backend/.venv` and dependencies were installed from `backend/requirements.txt`.
- `docker-compose up -d db` created and started `tft_analytics_postgres`.
- Docker volume name was pinned in `docker-compose.yml` with `name: tft_analytics_postgres_data`.
- `alembic upgrade head` succeeded against `tft_analytics_db`.
- `docker exec tft_analytics_postgres psql -U tft_analytics_user -d tft_analytics_db -c "\dt"` confirmed 20 tables including `alembic_version`.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` have identical file hashes.
- Repository is initialized on `main` and tracks `origin/main`.
- Frontend dependency install/build has not been run yet.

## 2026-05-20 Updates (2nd pass)

- `riot_tft_client.py`: `get_challenger_league`, `get_grandmaster_league`, `get_summoner_by_summoner_id` 메서드 추가.
- `tft_match_collector.py`: 챌린저/그마 리그 소환사 목록 수집 → PUUID 조회 → 매치 수집 전체 플로우 구현.
- `tft_stats_aggregator.py`: 시너지 fingerprint 기반 조합 그룹핑 → 점수 계산 → TftComp/TftCompStatsDaily upsert 전체 구현. 공통코드 TIER_LABEL 그룹 참조하여 티어 라벨 검증.
- `admin_service.py`: 매치 수집 잡을 FastAPI BackgroundTasks 패턴으로 분리. 독립 DB 세션 사용.
- `api/admin.py`: `collect_tft_matches` 엔드포인트를 async + BackgroundTasks로 변경.
- `scripts/seed_common_codes.py`: TIER_LABEL, JOB_LOG_LEVEL, JOB_STATUS, REGION, COMP_DIFFICULTY 공통코드 시드 등록. DB 적용 완료.
- `recommenders/early_game_recommender.py`: 난이도 판별 로직을 pick_rate 기반 함수로 분리.

## 2026-05-20 Updates

- Added `batch_job_logs` table via Alembic migration `202605200001`.
- `JobRepository` extended with `add_log()` and `list_logs()` methods.
- `AdminService` now writes step-level logs (INFO/WARN/ERROR) per job run.
- New `GET /api/admin/jobs/runs/{run_id}/logs` endpoint.
- New `CommonCodeRepository`, `CommonCodeService` implemented.
- Admin API extended: CRUD for code groups and codes under `/api/admin/codes/`.
- Frontend: `AdminJobsScreen` updated to show collapsible step logs per run.
- Frontend: `AdminCommonCodesScreen` and `/admin/codes` page added.
- `riot.txt` and `.nojekyll` committed for GitHub Pages Riot API verification.

## 2026-05-20 Bug Fixes (3rd pass)

- `riot_tft_client.py`: `get_account_by_puuid(puuid, routing)` 메서드 추가. `/riot/account/v1/accounts/by-puuid/{puuid}` 호출로 gameName/tagLine 조회.
- `tft_match_collector.py`:
  - 함수 내부 `db.commit()` 제거 → 트랜잭션 경계를 caller(`run_collection_background`)로 이관.
  - Riot Summoner API deprecated `name` 필드 사용 제거 → `get_account_by_puuid`로 gameName/tagLine 취득.
  - `except Exception: continue` 패턴에 `logger.warning(...)` 추가 (silent swallowing 제거).
- `admin_service.py`: `__import__("app.models.common", ...)` 안티패턴 제거 → 함수 내부 직접 `from app.models.common import BatchJobRun` 사용. 수집 완료 후 명시적 `db.commit()` 추가.
- `tft_stats_aggregator.py`: `date.today()` (timezone-naive) → `datetime.now(timezone.utc).date()` 로 수정.

## DB 상태 확인 (2026-05-20)

- 전체 21개 테이블 정상 존재 (`\dt` 확인).
- `batch_job_runs` 7컬럼, `batch_job_logs` 7컬럼, `tft_matches` 10컬럼, `tft_match_participants` 13컬럼, `tft_comps` 10컬럼, `tft_comp_stats_daily` 14컬럼 — 모두 모델과 일치.
- `batch_job_runs` 데이터 없음 (Riot API key 미설정으로 실제 수집 미실행).

## 2026-05-20 Updates (4th pass)

- `common_code_repository.py`: `list_groups()`에 `selectinload(CommonCodeGroup.codes)` 추가 → N+1 쿼리 제거.
- `common_code_service.py`: `list_groups()`에서 별도 `list_codes()` 루프 제거, 관계 직접 사용.
- `schemas/admin.py`: `CommonCodeGroupResponse`에 `model_config = {"from_attributes": True}` 추가.
- `requirements.txt`: `bcrypt==4.0.1` 핀 추가 (passlib 1.7.4 호환 버전).
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: 토큰 절약형으로 축약 (2045 → 989 chars, ~52% 감소).
- 배치 파이프라인 전체 API 경로 검증 완료:
  - `POST /api/admin/jobs/collect-tft-matches`: batch_job_runs/logs 정상 기록, 30소환사/250매치 수집 SUCCESS
  - `POST /api/admin/jobs/recalculate-tft-stats`: 66개 조합 통계 재계산 SUCCESS (2736경기 분석)

## DB 최종 현황 (2026-05-20)

| 테이블 | 건수 |
|---|---|
| batch_job_runs | 2 |
| batch_job_logs | 5 |
| riot_accounts | 49 |
| tft_summoners | 39 |
| tft_matches | 342 |
| tft_match_participants | 2,736 |
| tft_units | 24,056 |
| tft_traits | 29,557 |
| tft_comps | 66 |
| tft_comp_stats_daily | 66 |
| common_code_groups | 5 |
| common_codes | 19 |

## Next Work

- Add Riot API key to `backend/.env` (`RIOT_API_KEY=RGAPI-...`).
- Create an initial admin account with `python -m app.scripts.create_admin`.
- Run FastAPI locally and smoke-test auth endpoints.
- Install frontend dependencies (`npm install`) and run `npm run dev`.
- Implement unit-level item recommendation API and frontend screen.
- Implement unit/comp name search API with tier filter.
- Implement MCP server exposing TFT meta tools for AI assistants.
- Expand match normalization and meta aggregation with live data once Riot API key is active.
