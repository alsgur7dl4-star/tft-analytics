# TFT Analytics – AI Rules

## Data Safety
Never touch `jobfit-ai` resources. Project-only:
`tft_analytics_postgres` / `tft_analytics_db` / `tft_analytics_user` / `tft_analytics_postgres_data` / host port `5433`.
No secrets, API keys, or tokens in code or docs.

## Workflow
1. Read `HANDOFF.md` before any work.
2. `git status --short` before editing.
3. Update `HANDOFF.md` after completing work.
4. Keep `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` identical.

## Backend: `api → service → repository → model`
- Routers: HTTP only | Services: business logic | Repos: DB only
- Session: `deps.py` | Config: `core/config.py` | Riot API: `clients/riot_tft_client.py`
- Jobs: `app/jobs/` | Analytics: `app/analytics/` | Recommenders: `app/recommenders/`

## Frontend
- Routing: `src/app` | Screens: `src/screens` | API calls: `src/api`
- Axios: `withCredentials: true`, base URL from `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`)
- Auth-gated routes redirect anonymous users to `/login`
