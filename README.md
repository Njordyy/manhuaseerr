# ManhuaSeer v0.2 (Prod-leaning MVP)
- Postgres + Alembic
- API key auth (header: `x-api-key`)
- APScheduler background job to refresh/download followed series hourly
- Structured logs (Loguru)
- Docker Compose stack (db/api/web)

## Run
```bash
docker compose up -d --build
```
Open http://localhost:8085 (set API key input to match API_KEY env).

## ENV
- DATABASE_URL=postgresql+psycopg2://manhua:manhua_pass@db:5432/manhuadb
- API_KEY=changeme (set to strong secret in prod)
- JOB_INTERVAL_MINUTES=60
- DOWNLOAD_DIR=/downloads
- COMICK_API_ENABLED=true
- JOBS_ENABLED=true (toggle background scheduler)

## Migrations
Alembic is auto-applied via SQLAlchemy metadata in this cut; extend for real migration flows.
