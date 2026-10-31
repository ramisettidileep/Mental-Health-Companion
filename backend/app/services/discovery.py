import httpx
from app.core.config import settings


async def youtube_search(query: str, search_type: str = "videos") -> list[dict]:
    if not settings.youtube_api_key:
        raise RuntimeError(
            "YouTube discovery is not configured. "
            "Add YOUTUBE_API_KEY to backend/.env."
        )

    search_query = query

    if search_type == "podcasts":
        search_query = f"{query} podcast full episode"

    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "type": "video",
                "maxResults": 6,
                "q": search_query,
                "key": settings.youtube_api_key,
            },
        )
        response.raise_for_status()
        data = response.json().get("items", [])

    results = []

    for item in data:
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})

        if not video_id:
            continue

        thumbnails = snippet.get("thumbnails", {})

        results.append({
            "title": snippet.get("title", "Untitled video"),
            "description": snippet.get("description", "")[:260],
            "channel": snippet.get("channelTitle", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "image": (
                thumbnails.get("medium")
                or thumbnails.get("default")
                or {}
            ).get("url"),
        })

    return results


async def youtube_podcasts(query: str) -> list[dict]:
    return await youtube_search(query, search_type="podcasts")


async def youtube_videos(query: str) -> list[dict]:
    return await youtube_search(query, search_type="videos")