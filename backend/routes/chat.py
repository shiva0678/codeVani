"""
Chat Routes — Handles Q&A conversations about repositories.

Endpoints:
  POST /chat — Accepts a question (+ optional language),
               returns answer, translated answer, and audio URL.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ai_service import answer_question
from services.translation_service import translate_text
from services.tts_service import text_to_speech, cleanup_old_files

router = APIRouter()

# ── In-memory context store ──────────────────────────────────
# Stores the current repo context for chat. In production,
# you'd use sessions/DB, but this works for an MVP.
_repo_context: str = ""


def set_repo_context(context: str):
    """Update the stored repo context (called after /analyze)."""
    global _repo_context
    _repo_context = context


def get_repo_context() -> str:
    """Retrieve the current repo context."""
    return _repo_context


# ── Request/Response Models ──────────────────────────────────

class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""
    question: str
    language: Optional[str] = "en"  # 'en', 'hi', or 'kn'
    context: Optional[str] = None   # Optional override for repo context


class ChatResponse(BaseModel):
    """Response from chat endpoint with answer + translation + audio."""
    answer: str               # Original English answer
    translated_answer: str    # Translated answer (same as answer if lang='en')
    language: str             # Language code used
    audio_url: Optional[str]  # URL to the generated audio file


# ── Endpoints ────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Answer a question about the analyzed repository.

    1. Use stored repo context (or provided context) as background
    2. Generate answer using Gemini AI
    3. Translate to requested language
    4. Convert translated text to speech
    5. Return everything to the frontend
    """
    # Determine which context to use
    context = request.context or get_repo_context()

    if not context:
        raise HTTPException(
            status_code=400,
            detail="No repository context available. Please analyze a repo first."
        )

    try:
        # Step 1: Get AI answer in English
        answer = answer_question(context, request.question)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI failed to generate answer: {str(e)}"
        )

    # Step 2: Translate if needed
    lang = request.language or "en"
    translated = translate_text(answer, lang)

    # Step 3: Generate speech from the translated text
    audio_url = None
    try:
        filename = text_to_speech(translated, lang)
        audio_url = f"/audio/{filename}"

        # Clean up old files to prevent disk bloat
        cleanup_old_files()
    except Exception as e:
        print(f"[TTS Warning] Could not generate audio: {e}")
        # Don't fail the whole request if TTS fails — audio is optional

    return ChatResponse(
        answer=answer,
        translated_answer=translated,
        language=lang,
        audio_url=audio_url,
    )
