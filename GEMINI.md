# TFT Analytics AI Handoff Rules

## Project

This repository is a new TFT analytics service: Riot API based TFT match lookup, meta composition analytics, and recommender features for early-game units and artifacts/items.

## Critical Data Safety

- Never modify, delete, mount, migrate, or copy any real `jobfit-ai` database, DB user, Docker volume, user data, refresh token data, token data, or domain data.
- Use only the dedicated project resources:
  - Docker container: `tft_analytics_postgres`
  - DB: `tft_analytics_db`
  - DB user: `tft_analytics_user`
  - Docker volume: `tft_analytics_postgres_data`
  - Host port: `5433`, container port: `5432`
- Do not write secrets, Riot API keys, JWT secrets, tokens, or passwords in code or documentation.

## Required Workflow

- Read `HANDOFF.md` before starting work.
- Run `git status --short` before editing when this directory is a git repository.
- Update `HANDOFF.md` after completing work.
- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` identical. If one changes, update all three.

## Architecture Rules

- Backend follows `api -> service -> repository -> model`.
- API routers handle request/response only.
- Services own business logic and use repositories for DB access.
- Repositories contain DB access only.
- ORM models and Pydantic schemas stay separate.
- DB sessions are injected through `backend/app/api/deps.py`.
- Settings are read only from `backend/app/core/config.py`.
- Riot API calls go through `backend/app/clients/riot_tft_client.py`.
- Collection jobs live in `backend/app/jobs/`.
- Analytics logic lives in `backend/app/analytics/`.
- Recommendation logic lives in `backend/app/recommenders/`.

## Frontend Rules

- `frontend/src/app` is the routing entrypoint.
- Screen logic lives in `frontend/src/screens`.
- API calls live in `frontend/src/api`.
- Authenticated features require login and redirect anonymous users to `/login`.
- Axios must use `withCredentials: true`.
- API base URL comes from `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:8000`.

