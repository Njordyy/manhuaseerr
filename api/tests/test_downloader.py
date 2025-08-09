from pathlib import Path
import tempfile
import zipfile
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.downloader import download_chapters


def test_download_chapters_creates_cbz_with_readme():
    chapters = [
        {"num": "1", "title": "Chapter 1"},
        {"num": "2", "title": "Chapter 2"},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        created = download_chapters(Path(tmpdir), "series1", chapters)
        assert len(created) == len(chapters)
        for path, chap in zip(created, chapters):
            p = Path(path)
            assert p.exists()
            with zipfile.ZipFile(p) as z:
                with z.open("README.txt") as f:
                    content = f.read().decode()
                    assert chap["title"] in content


def test_download_chapters_sanitizes_series_key():
    chapters = [{"num": "1", "title": "One"}]
    with tempfile.TemporaryDirectory() as tmpdir:
        created = download_chapters(Path(tmpdir), "../evil", chapters)
        assert len(created) == 1
        p = Path(created[0]).resolve()
        assert p.is_relative_to(Path(tmpdir).resolve())
