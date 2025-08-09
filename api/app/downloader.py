from zipfile import ZipFile
import io
import datetime as dt
from pathlib import Path
from typing import List, Dict

# Placeholder downloader: creates CBZ with a README per chapter.
# TODO: Replace with real image fetch logic for Comick chapters.

def download_chapters(download_dir: Path, series_key: str, chapters: List[Dict]):
    series_dir = download_dir / series_key
    series_dir.mkdir(parents=True, exist_ok=True)
    created = []
    for c in chapters:
        cbz_path = series_dir / f"{c['num']}.cbz"
        mem = io.BytesIO()
        with ZipFile(mem, 'w') as z:
            z.writestr("README.txt", f"Placeholder for {c['title']} created {dt.datetime.utcnow().isoformat()}Z\n")
        with open(cbz_path, 'wb') as f:
            f.write(mem.getvalue())
        created.append(str(cbz_path))
    return created
