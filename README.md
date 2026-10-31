# Stillwell — AI Mental Health Companion

Stillwell is a privacy-conscious emotional-support companion built with Next.js and FastAPI. It supports text conversations, browser-native voice input/output, optional AI-generated reflective stories, and real Spotify/YouTube discovery when API credentials are configured.

> Stillwell offers general emotional support. It is not a therapist, diagnostic tool, emergency service, or substitute for professional care.

## Features in this starter
- Groq-powered conversational support with short, bounded conversation context.
- Safety-oriented handling for messages that may indicate immediate self-harm danger.
- Browser speech recognition and speech synthesis, with visible states and graceful unsupported-browser handling.
- AI-generated fictional stories on demand.
- Spotify podcast search and YouTube video search endpoints (real APIs; credentials required).
- Editorial responsive UI, backend input validation, CORS configuration, bounded outputs, tests, and environment examples.

## Requirements
- Node.js 20+ and npm
- Python 3.11+
- A Groq API key for AI responses: create/manage it in your Groq account.
- Optional Spotify app credentials and YouTube Data API key for discovery.

## Run locally

### 1. Configure backend
```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `backend/.env` and set `GROQ_API_KEY`. Keep secrets private and never commit `.env`.

### 2. Start API
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### 3. Start frontend in another terminal
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
Open http://localhost:3000.

## Configuration
Backend values are documented in `backend/.env.example`. `GROQ_MODEL` is configurable; verify current model availability in your Groq account/docs before selecting a model. The starter default is `openai/gpt-oss-20b`, listed by Groq as a production model with JSON-mode support; availability can still depend on your account and may change. Spotify and YouTube features return a clear setup error if their credentials are absent.

Frontend `NEXT_PUBLIC_API_BASE_URL` defaults to `http://localhost:8000`.

## Voice
Voice input uses browser `SpeechRecognition` / `webkitSpeechRecognition` when available. Support differs by browser. Speech is sent as text to the backend after recognition; the browser's speech synthesis reads responses aloud. This starter does not upload or persist raw audio. Microphone access is requested only after the user clicks the microphone control. Use localhost or HTTPS for browser microphone permissions.

## Safety and privacy
- No authentication or database is included in this first runnable milestone. Conversations are held in frontend memory and are not persisted by the app. Refreshing the page clears the current session.
- Never put API secrets in frontend environment variables.
- The safety logic is a basic precaution, not a clinically validated risk detector. If someone is in immediate danger, contact local emergency services and a trusted person. In India, emergency assistance can be reached at 112; verify current local resources for your situation.
- Do not use this product as a substitute for professional mental-health care.

## Tests and checks
```bash
cd backend
pytest
```
Frontend checks:
```bash
cd frontend
npm run lint
npm run build
```

Unit tests use mocked AI/network boundaries where appropriate. Live Groq, Spotify and YouTube integrations still require valid credentials and separate real-world verification. No live integration is claimed as tested by this generated source package.

## Current limitations
- No login, PostgreSQL persistence, saved stories, or long-term memory yet.
- Browser voice support and voices vary; text remains available as fallback.
- Crisis handling is intentionally conservative but cannot reliably identify every crisis.
- External discovery requires valid API credentials and is subject to provider access, quota, and policy limits.
- Do not deploy publicly without adding authentication/authorization, abuse controls, stronger monitoring, and a reviewed crisis-resource policy.
