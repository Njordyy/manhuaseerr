import httpx
from typing import List, Dict, Any

API_BASES = [
    "https://api.comick.io",
    "https://comick.io/api"
]

class ComickClient:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    async def search(self, q: str) -> List[Dict[str, Any]]:
        if not self.enabled:
            return [{"id": "demo-1", "title": "Demo Comick Series", "cover": None, "source": "comick", "chapters": None, "genres": [], "status": "Ongoing"}]
        for base in API_BASES:
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    r = await client.get(f"{base}/v1.0/search", params={"q": q})
                    if r.status_code == 200:
                        data = r.json()
                        out = []
                        for it in data:
                            out.append({
                                "id": it.get("hid") or it.get("slug") or str(it.get("id")),
                                "title": it.get("title") or (it.get("md_titles", [{}])[0].get("title") if it.get("md_titles") else "Unknown"),
                                "cover": it.get("cover_url"),
                                "source": "comick",
                                "chapters": None,
                                "genres": [],
                                "status": it.get("status")
                            })
                        return out
            except Exception:
                continue
        return []

    async def chapters(self, series_id: str) -> List[Dict[str, Any]]:
        for base in API_BASES:
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    r = await client.get(f"{base}/v1.0/chapter", params={"mhid": series_id, "lang": "en"})
                    if r.status_code == 200 and isinstance(r.json(), list):
                        arr = r.json()
                        return [{
                            "id": str(c.get("hid") or c.get("id") or c.get("chapter")),
                            "num": str(c.get("chap", c.get("chapter", "0"))),
                            "title": c.get("title") or f"Chapter {c.get('chap', c.get('chapter', '0'))}"
                        } for c in arr]
            except Exception:
                continue
        return [{"id": "c1", "num": "1", "title": "Demo Chapter 1"}]
