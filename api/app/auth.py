from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("API_KEY", "changeme")

async def require_api_key(x_api_key: str = Header(None)):
    if not API_KEY or API_KEY == "changeme":
        return  # disabled in dev
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
