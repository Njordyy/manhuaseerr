# ManhuaSeer v0.2 (Prod-leaning MVP)
- Postgres + Alembic
- API key auth (header: `x-api-key`)
- APScheduler background job to refresh/download followed series hourly
- Structured logs (Loguru)
- Docker Compose stack (db/api/web)
- API and web images pulled from GitHub Container Registry (override via `API_IMAGE`/`WEB_IMAGE`)

## Run
```bash
docker compose up -d
```
Compose defaults to `ghcr.io/manhuaseerr/api:latest` and `ghcr.io/manhuaseerr/web:latest` but honors `API_IMAGE` and `WEB_IMAGE` environment variables so you can point to images in your own repository. Authenticate to private GitHub packages with:

```bash
docker login ghcr.io -u <user> -p <token>
```

Open http://localhost:8085 (set API key input to match `API_KEY` env). Downloads are persisted in a named volume (`downloads_data`).

## ENV
- DATABASE_URL=postgresql+psycopg2://manhua:manhua_pass@db:5432/manhuadb
- API_KEY=changeme (set to strong secret in prod)
- JOB_INTERVAL_MINUTES=60
- DOWNLOAD_DIR=/downloads (mounted from `downloads_data` volume)
- COMICK_API_ENABLED=true
- JOBS_ENABLED=true (toggle background scheduler)

## Migrations
Alembic is auto-applied via SQLAlchemy metadata in this cut; extend for real migration flows.
