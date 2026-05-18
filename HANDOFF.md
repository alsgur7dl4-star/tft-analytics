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

## Next Work

- Add Riot API key locally and test Account/Match API calls.
- Create an initial admin account with `python -m app.scripts.create_admin`.
- Run FastAPI locally and smoke-test auth endpoints.
- Install frontend dependencies and run `npm run dev`.
- Expand match normalization and meta aggregation with live data.
