import json
from app.core.config import settings
from app.prompts.companion import COMPANION_SYSTEM, STORY_SYSTEM
from app.schemas.chat import Message

class AIUnavailable(RuntimeError):
    pass

def _client():
    try:
        from groq import AsyncGroq
    except ImportError as exc:
        raise AIUnavailable("Groq SDK is not installed. Run pip install -r requirements.txt.") from exc
    if not settings.groq_api_key:
        raise AIUnavailable("Groq is not configured. Add GROQ_API_KEY to backend/.env.")
    return AsyncGroq(api_key=settings.groq_api_key, timeout=30.0, max_retries=1)

async def respond(message: str, history: list[Message], support_style: str) -> str:
    client = _client()
    messages = [{"role": "system", "content": COMPANION_SYSTEM + f"\nRequested support style: {support_style}."}]
    # Bound context to the last 12 turns and clip each entry to control token use.
    for item in history[-12:]:
        messages.append({"role": item.role, "content": item.content[:2500]})
    messages.append({"role": "user", "content": message})
    try:
        result = await client.chat.completions.create(
            model=settings.groq_model, messages=messages, temperature=0.65, max_tokens=500,
        )
        text = result.choices[0].message.content
        if not text or not text.strip():
            raise AIUnavailable("The AI returned an empty response. Please try again.")
        return text.strip()
    except AIUnavailable:
        raise
    except Exception as exc:
        # Don't leak upstream response details or user content.
        raise AIUnavailable("The AI service is temporarily unavailable. Check your model/key configuration and try again.") from exc

async def make_story(situation: str, tone: str, length: str) -> dict:
    client = _client()
    try:
        result = await client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role":"system","content":STORY_SYSTEM + f" Tone: {tone}. Length: {length}."},
                      {"role":"user","content":situation}],
            temperature=0.8, max_tokens=650, response_format={"type":"json_object"},
        )
        raw = result.choices[0].message.content or "{}"
        data = json.loads(raw)
        if not all(isinstance(data.get(k), str) and data[k].strip() for k in ("title", "story", "reflection")):
            raise ValueError("Missing story fields")
        return {"title": data["title"][:160], "story": data["story"][:6000], "reflection": data["reflection"][:500], "fictional": True}
    except Exception as exc:
        raise AIUnavailable("Story generation failed. Please try again in a moment.") from exc
