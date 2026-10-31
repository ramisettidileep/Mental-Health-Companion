import base64, time
import httpx
from app.core.config import settings

_spotify_token: tuple[str, float] | None = None

async def spotify_podcasts(query: str) -> list[dict]:
    global _spotify_token
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise RuntimeError("Spotify discovery is not configured. Add Spotify client credentials to backend/.env.")
    now = time.time()
    if not _spotify_token or _spotify_token[1] < now + 60:
        auth = base64.b64encode(f"{settings.spotify_client_id}:{settings.spotify_client_secret}".encode()).decode()
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post("https://accounts.spotify.com/api/token", headers={"Authorization": f"Basic {auth}"}, data={"grant_type":"client_credentials"})
            response.raise_for_status()
            payload = response.json()
            _spotify_token = (payload["access_token"], now + int(payload.get("expires_in", 3600)))
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get("https://api.spotify.com/v1/search", headers={"Authorization": f"Bearer {_spotify_token[0]}"}, params={"q":query,"type":"show","limit":6})
        response.raise_for_status()
        data = response.json().get("shows", {}).get("items", [])
    return [{"title":x.get("name","Untitled show"),"description":(x.get("description") or "")[:260],"url":(x.get("external_urls") or {}).get("spotify",""),"image":((x.get("images") or [{}])[0]).get("url"),"publisher":x.get("publisher","")} for x in data if x]

async def youtube_videos(query: str) -> list[dict]:
    if not settings.youtube_api_key:
        raise RuntimeError("YouTube discovery is not configured. Add YOUTUBE_API_KEY to backend/.env.")
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get("https://www.googleapis.com/youtube/v3/search", params={"part":"snippet","type":"video","maxResults":6,"q":query,"key":settings.youtube_api_key})
        response.raise_for_status()
        data = response.json().get("items", [])
    out=[]
    for x in data:
        ident=x.get("id",{}).get("videoId")
        snippet=x.get("snippet",{})
        if ident:
            thumbs=snippet.get("thumbnails",{})
            out.append({"title":snippet.get("title","Untitled video"),"description":snippet.get("description","")[:260],"channel":snippet.get("channelTitle",""),"url":f"https://www.youtube.com/watch?v={ident}","image":(thumbs.get("medium") or thumbs.get("default") or {}).get("url")})
    return out
