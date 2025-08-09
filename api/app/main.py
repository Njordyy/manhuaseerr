from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from .sources.comick import ComickClient
from .sources.asura import AsuraClient
from .db import SessionLocal, Series
from .auth import require_api_key
from .downloader import download_chapters
from .jobs import start_scheduler
from pathlib import Path
import os
from loguru import logger

app = FastAPI(title="Manhuaseerr API")

# CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

COMICK_ENABLED = os.getenv("COMICK_API_ENABLED", "true").lower() == "true"
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "/downloads"))
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
API_KEY_ENABLED = os.getenv("API_KEY", "changeme") != "changeme"

comick = ComickClient(enabled=COMICK_ENABLED)
asura = AsuraClient(enabled=False)

class SeriesOut(BaseModel):
    id: str
    title: str
    cover: Optional[str] = None
    source: str
    chapters: Optional[int] = None
    genres: Optional[List[str]] = None
    status: Optional[str] = None

class FollowIn(BaseModel):
    id: str
    title: str
    cover: Optional[str] = None
    source: str

@app.on_event("startup")
async def startup():
    if os.getenv("JOBS_ENABLED", "true").lower() == "true":
        interval = int(os.getenv("JOB_INTERVAL_MINUTES", "60"))
        start_scheduler(interval, DOWNLOAD_DIR)
        logger.info(f"Scheduler started with interval {interval} minutes")

@app.get("/api/health")
async def health():
    return {"ok": True}

@app.get("/api/search", response_model=List[SeriesOut])
async def search(q: str = Query(..., min_length=2), source: str = Query("all"), auth=Depends(require_api_key)):
    results: List[SeriesOut] = []
    if source in ("all", "comick"):
        results += await comick.search(q)
    if source in ("all", "asura"):
        results += await asura.search(q)
    dedup = {}
    for r in results:
        dedup[(r["source"], r["id"])] = r
    return list(dedup.values())

@app.post("/api/follow", response_model=SeriesOut)
async def follow(payload: FollowIn, db: Session = Depends(get_db), auth=Depends(require_api_key)):
    s = db.query(Series).filter(Series.source==payload.source, Series.remote_id==payload.id).first()
    if not s:
        s = Series(source=payload.source, remote_id=payload.id, title=payload.title, cover=payload.cover)
        db.add(s)
        db.commit()
        db.refresh(s)
    return SeriesOut(id=s.remote_id, title=s.title, cover=s.cover, source=s.source)

@app.get("/api/following", response_model=List[SeriesOut])
async def following(db: Session = Depends(get_db), auth=Depends(require_api_key)):
    items = db.query(Series).all()
    return [SeriesOut(id=i.remote_id, title=i.title, cover=i.cover, source=i.source) for i in items]

@app.get("/api/series/{source}/{series_id}/chapters")
async def chapters(source: str, series_id: str, auth=Depends(require_api_key)):
    if source == "comick":
        return await comick.chapters(series_id)
    if source == "asura":
        return await asura.chapters(series_id)
    raise HTTPException(404, "Unknown source")

class DownloadIn(BaseModel):
    source: str
    series_id: str
    chapters: Optional[List[str]] = None

@app.post("/api/download")
async def download(payload: DownloadIn, auth=Depends(require_api_key)):
    if payload.source == "comick":
        chs = await comick.chapters(payload.series_id)
    elif payload.source == "asura":
        chs = await asura.chapters(payload.series_id)
    else:
        raise HTTPException(400, "Unknown source")
    chosen = [c for c in chs if (not payload.chapters or c["id"] in payload.chapters)]
    created = download_chapters(DOWNLOAD_DIR, f"{payload.source}_{payload.series_id}", chosen)
    return {"created": created}
