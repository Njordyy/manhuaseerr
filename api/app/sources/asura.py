class AsuraClient:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    async def search(self, q: str):
        return []

    async def chapters(self, series_id: str):
        return []
