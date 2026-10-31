from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.chat import router as chat_router
from app.api.routes.discover import router as discover_router

app = FastAPI(
    title="Stillwell API",
    version="0.1.0",
    description="General emotional-support companion API",
)

# Development CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(discover_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "stillwell-api",
        "groq_configured": bool(settings.groq_api_key),
    }