from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from .db import SessionLocal, Series
from .sources.comick import ComickClient
from .sources.asura import AsuraClient
from .downloader import download_chapters
from pathlib import Path
import os
from loguru import logger

def start_scheduler(interval_minutes: int, download_dir: Path):
    scheduler = AsyncIOScheduler(timezone="UTC")

    async def refresh_and_download():
        logger.info("Job: refresh_and_download starting")
        db: Session = SessionLocal()
        try:
            items = db.query(Series).all()
            comick = ComickClient(enabled=True)
            asura = AsuraClient(enabled=False)
            for s in items:
                try:
                    if s.source == "comick":
                        chs = await comick.chapters(s.remote_id)
                    elif s.source == "asura":
                        chs = await asura.chapters(s.remote_id)
                    else:
                        chs = []
                    if chs:
                        series_key = f"{s.source}_{s.remote_id}"
                        created = download_chapters(download_dir, series_key, chs)
                        logger.info(f"Downloaded/created {len(created)} files for {s.title}")
                except Exception as e:
                    logger.exception(f"Failed job for series {s.title}: {e}")
        finally:
            db.close()
        logger.info("Job: refresh_and_download finished")

    scheduler.add_job(refresh_and_download, IntervalTrigger(minutes=interval_minutes), id="refresh_download", replace_existing=True)
    scheduler.start()
    return scheduler
