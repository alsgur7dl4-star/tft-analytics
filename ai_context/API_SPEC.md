# API Spec

Base URL: `http://localhost:8000`

All primary TFT, recommendation, and admin endpoints require an authenticated user. Admin endpoints require `ADMIN`.

## Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

## Auth

### `POST /api/auth/register`

Request:

```json
{
  "email": "user@example.com",
  "password": "password",
  "nickname": "nickname"
}
```

### `POST /api/auth/login`

Sets `refresh_token` as an HttpOnly cookie and returns an access token.

### `POST /api/auth/refresh`

Rotates refresh token and returns a new access token.

### `POST /api/auth/logout`

Revokes the current refresh token cookie.

### `GET /api/auth/me`

Returns the current authenticated user.

## TFT Lookup

- `GET /api/tft/accounts/search?game_name={gameName}&tag_line={tagLine}&region=KR`
- `GET /api/tft/summoners/{puuid}`
- `GET /api/tft/summoners/{puuid}/matches`
- `GET /api/tft/matches/{match_id}`

## Meta

- `GET /api/tft/meta/comps`
- `GET /api/tft/meta/comps/{comp_id}`
- `GET /api/tft/meta/units`
- `GET /api/tft/meta/items`
- `GET /api/tft/meta/augments`

## Recommendations

### `POST /api/tft/recommendations/early-game`

Request:

```json
{
  "units": ["TFT_Unit_A", "TFT_Unit_B"],
  "items": ["Guinsoo's Rageblade"],
  "augments": ["Combat Caster"]
}
```

### `POST /api/tft/recommendations/artifacts`

Request:

```json
{
  "items": ["Trickster's Glass", "Infinity Force"]
}
```

## Admin

- `POST /api/admin/jobs/collect-tft-matches`
- `POST /api/admin/jobs/recalculate-tft-stats`
- `GET /api/admin/jobs/runs`
- `GET /api/admin/data-sources`

