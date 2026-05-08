"""
CodeVani Lite — Main FastAPI Application

This is the entry point for the backend server. It:
  1. Configures CORS for frontend communication
  2. Serves static audio files for TTS playback
  3. Mounts route modules for /analyze and /chat endpoints
  4. Provides a health check endpoint

Run with: uvicorn main:app --reload --port 8000
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import route modules
from routes.repo import router as repo_router
from routes.chat import router as chat_router, set_repo_context
from routes.repo import AnalyzeRequest
from services.github_service import fetch_repo_info, fetch_readme
from services.ai_service import summarize_repo

# ── App Configuration ────────────────────────────────────────

app = FastAPI(
    title="CodeVani Lite",
    description="AI-powered GitHub repository analyzer with translation and TTS",
    version="1.0.0",
)

# ── CORS Middleware ──────────────────────────────────────────
# Allow the React frontend (running on port 5173) to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files (Audio) ────────────────────────────────────
# Serve generated TTS audio files at /audio/filename.mp3
audio_dir = os.path.join(os.path.dirname(__file__), "audio_files")
os.makedirs(audio_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")

# ── Mount Routes ─────────────────────────────────────────────
app.include_router(repo_router, tags=["Repository"])
app.include_router(chat_router, tags=["Chat"])


# ── Override /analyze to also set chat context ───────────────
# We need to hook into the analyze flow to store context for chat
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


@app.post("/analyze-with-context")
async def analyze_with_context(request: AnalyzeRequest):
    """
    Wrapper around /analyze that also stores the repo context
    for subsequent chat questions.
    """
    try:
        # Fetch repo data
        repo_info = fetch_repo_info(request.github_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch repo: {str(e)}")

    try:
        readme = fetch_readme(request.github_url)
    except Exception:
        readme = "(Could not fetch README)"

    try:
        # Generate AI summary
        ai_result = summarize_repo(repo_info, readme)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {str(e)}")

    # Build context string for chat
    context = f"""
Repository: {repo_info.get('full_name', 'Unknown')}
Description: {repo_info.get('description', 'N/A')}
Language: {repo_info.get('language', 'Unknown')}

Summary: {ai_result.get('summary', '')}

Tech Stack: {ai_result.get('tech_stack', '')}

Setup: {ai_result.get('setup_instructions', '')}

README:
{readme}
"""
    # Store context for chat endpoint
    set_repo_context(context)

    return {
        "repo_name": repo_info.get("full_name", "Unknown"),
        "description": repo_info.get("description", "") or "No description",
        "language": repo_info.get("language", "Unknown") or "Unknown",
        "stars": repo_info.get("stars", 0),
        "summary": ai_result.get("summary", ""),
        "tech_stack": ai_result.get("tech_stack", ""),
        "setup_instructions": ai_result.get("setup_instructions", ""),
    }


# ── Health Check ─────────────────────────────────────────────

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "app": "CodeVani Lite",
        "version": "1.0.0",
        "endpoints": ["/analyze-with-context", "/chat", "/audio/{filename}"],
    }


# ── Run Server ───────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
