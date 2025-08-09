# ManhuaSeer v0.2 (Prod-leaning MVP)
- Postgres + Alembic
- API key auth (header: `x-api-key`)
- APScheduler background job to refresh/download followed series hourly
- Structured logs (Loguru)
- Docker Compose stack (db/api/web)
- API and web images pulled from GitHub Container Registry
- Web UI styling inspired by the Overseerr project

## Run
```bash
docker compose pull
docker compose up -d
```
Compose pulls `ghcr.io/Njordyy/manhuaseerr-api:main` and `ghcr.io/Njordyy/manhuaseerr-web:main` (images use `pull_policy: always`). Authenticate to private GitHub packages with:

```bash
docker login ghcr.io -u <user> -p <token>
```

Open http://localhost:8085 (set API key input to match `API_KEY` env). Downloads are persisted in a named volume (`downloads_data`).
The web container talks to the API at `http://api:8000` via `VITE_API_BASE`.

## ENV
- DATABASE_URL=postgresql+psycopg2://manhua:manhua_pass@db:5432/manhuadb
- API_KEY=changeme (set to strong secret in prod)
- JOB_INTERVAL_MINUTES=60
- DOWNLOAD_DIR=/downloads (mounted from `downloads_data` volume)
- COMICK_API_ENABLED=true
- JOBS_ENABLED=true (toggle background scheduler)

## Migrations
Alembic is auto-applied via SQLAlchemy metadata in this cut; extend for real migration flows.
