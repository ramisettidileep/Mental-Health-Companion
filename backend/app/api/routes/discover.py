from fastapi import APIRouter, HTTPException
import httpx
from app.schemas.chat import DiscoveryRequest
from app.services.discovery import spotify_podcasts, youtube_videos
router=APIRouter(prefix="/api/v1/discover", tags=["discovery"])

@router.post("/podcasts")
async def podcasts(body: DiscoveryRequest):
    try: return {"items": await spotify_podcasts(body.query)}
    except RuntimeError as e: raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e: raise HTTPException(status_code=502, detail="Spotify returned an error. Check credentials, API access, and try later.") from e
    except httpx.HTTPError as e: raise HTTPException(status_code=502, detail="Spotify could not be reached. Try again later.") from e

@router.post("/videos")
async def videos(body: DiscoveryRequest):
    try: return {"items": await youtube_videos(body.query)}
    except RuntimeError as e: raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e: raise HTTPException(status_code=502, detail="YouTube returned an error. Check the API key, quota, and try later.") from e
    except httpx.HTTPError as e: raise HTTPException(status_code=502, detail="YouTube could not be reached. Try again later.") from e
