from zipfile import ZipFile
import io
import datetime as dt
from pathlib import Path
from typing import List, Dict

# Placeholder downloader: creates CBZ with a README per chapter.
# TODO: Replace with real image fetch logic for Comick chapters.

def download_chapters(download_dir: Path, series_key: str, chapters: List[Dict]):
    """Create placeholder CBZ files for the requested chapters.

    A series key might originate from user input or an external API.  To avoid
    path traversal, only the final path segment is used when constructing the
    directory for the series.
    """

    base_dir = download_dir.resolve()
    series_dir = (base_dir / Path(series_key).name).resolve()
    if not series_dir.is_relative_to(base_dir):
        raise ValueError("Invalid series key")

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
