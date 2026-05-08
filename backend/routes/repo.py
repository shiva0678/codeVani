"""
Repo Routes — Handles GitHub repository analysis.

Endpoints:
  POST /analyze — Accepts a GitHub URL, fetches repo data,
                   and returns an AI-generated summary.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_service import fetch_repo_info, fetch_readme
from services.ai_service import summarize_repo

router = APIRouter()


# ── Request/Response Models ──────────────────────────────────

class AnalyzeRequest(BaseModel):
    """Request body for the /analyze endpoint."""
    github_url: str


class AnalyzeResponse(BaseModel):
    """Structured response from repo analysis."""
    repo_name: str
    description: str
    language: str
    stars: int
    summary: str
    tech_stack: str
    setup_instructions: str


# ── Endpoints ────────────────────────────────────────────────

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repo(request: AnalyzeRequest):
    """
    Analyze a GitHub repository.

    1. Fetch repo metadata from GitHub API
    2. Fetch README.md content
    3. Send to Gemini AI for structured analysis
    4. Return summary, tech stack, and setup instructions
    """
    try:
        # Step 1: Fetch repo info from GitHub
        repo_info = fetch_repo_info(request.github_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch repository info: {str(e)}"
        )

    try:
        # Step 2: Fetch README content
        readme = fetch_readme(request.github_url)
    except Exception:
        readme = "(Could not fetch README)"

    try:
        # Step 3: Generate AI summary
        ai_result = summarize_repo(repo_info, readme)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI analysis failed: {str(e)}"
        )

    # Step 4: Return structured response
    return AnalyzeResponse(
        repo_name=repo_info.get("full_name", "Unknown"),
        description=repo_info.get("description", "") or "No description",
        language=repo_info.get("language", "Unknown") or "Unknown",
        stars=repo_info.get("stars", 0),
        summary=ai_result.get("summary", ""),
        tech_stack=ai_result.get("tech_stack", ""),
        setup_instructions=ai_result.get("setup_instructions", ""),
    )
