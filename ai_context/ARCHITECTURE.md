# Architecture

## Overview

TFT Analytics is split into a FastAPI backend, Next.js frontend, and isolated PostgreSQL 16 Docker database.

The backend uses a layered architecture:

```text
api -> services -> repositories -> models
```

External Riot API traffic is isolated in `backend/app/clients/riot_tft_client.py`. Collection jobs are in `backend/app/jobs`, statistical logic is in `backend/app/analytics`, and recommendation scoring is in `backend/app/recommenders`.

## Backend Layout

```text
backend/app/
  api/            FastAPI routers and dependencies
  services/       Business logic
  repositories/   SQLAlchemy DB access
  models/         SQLAlchemy ORM models
  schemas/        Pydantic DTOs
  core/           Settings, DB, security, exceptions
  clients/        Riot API client
  jobs/           Batch collection and aggregation jobs
  analytics/      Meta/player statistics
  recommenders/   Early-game and artifact recommender logic
  scripts/        Manual scripts
```

## Frontend Layout

```text
frontend/src/
  app/          Next.js App Router routes
  screens/      Page-level screen components
  components/   Shared layout and UI components
  api/          Axios client and API functions
  stores/       Auth and global client state
  lib/          Utilities
  styles/       Global CSS
```

## Authentication

- Access tokens are JWT bearer tokens with a default 15 minute lifetime.
- Refresh tokens are random strings stored in HttpOnly cookies.
- Only SHA-256 refresh token hashes are stored in the database.
- Main product pages require login.
- User roles are `USER` and `ADMIN`.

## Database Isolation

This project uses only:

- `tft_analytics_postgres`
- `tft_analytics_db`
- `tft_analytics_user`
- `tft_analytics_postgres_data`

No `jobfit-ai` DB, user, volume, token, or user data is referenced.

