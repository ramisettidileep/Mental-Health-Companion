import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.chat import DiscoveryRequest
from app.services.discovery import youtube_podcasts, youtube_videos

router = APIRouter(prefix="/api/v1/discover", tags=["discovery"])


@router.post("/podcasts")
async def podcasts(body: DiscoveryRequest):
    try:
        return {"items": await youtube_podcasts(body.query)}

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail="YouTube returned an error. Check the API key, quota, and try again.",
        ) from error

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="YouTube could not be reached. Try again later.",
        ) from error


@router.post("/videos")
async def videos(body: DiscoveryRequest):
    try:
        return {"items": await youtube_videos(body.query)}

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail="YouTube returned an error. Check the API key, quota, and try again.",
        ) from error

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="YouTube could not be reached. Try again later.",
        ) from error