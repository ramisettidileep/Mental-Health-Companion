from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, StoryRequest, StoryResponse
from app.services.groq_service import respond, make_story, AIUnavailable
from app.services.safety import may_be_crisis, CRISIS_NOTICE

router = APIRouter(prefix="/api/v1", tags=["companion"])

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    if may_be_crisis(body.message):
        return ChatResponse(reply=CRISIS_NOTICE, safety_notice="Safety support shown. This is not emergency care.")
    try:
        reply = await respond(body.message, body.history, body.support_style)
        return ChatResponse(reply=reply)
    except AIUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@router.post("/stories", response_model=StoryResponse)
async def story(body: StoryRequest):
    try:
        return await make_story(body.situation, body.tone, body.length)
    except AIUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
