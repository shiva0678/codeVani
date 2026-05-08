"""
GitHub Service — Fetches repository data from GitHub API.

Uses the GitHub REST API to extract:
  - Repository metadata (name, description, stars, language)
  - README.md content (decoded from base64)
"""

import os
import re
import base64
import requests


def _parse_github_url(url: str) -> tuple[str, str]:
    """
    Extract owner and repo name from a GitHub URL.
    Supports formats like:
      - https://github.com/owner/repo
      - https://github.com/owner/repo.git
      - github.com/owner/repo
    """
    # Remove trailing slashes and .git suffix
    url = url.strip().rstrip("/").removesuffix(".git")

    # Match github.com/owner/repo pattern
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError(
            f"Invalid GitHub URL: {url}. "
            "Expected format: https://github.com/owner/repo"
        )
    return match.group(1), match.group(2)


def _get_headers() -> dict:
    """Build request headers, optionally including a GitHub token."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_repo_info(github_url: str) -> dict:
    """
    Fetch repository metadata from the GitHub API.

    Returns a dict with: name, full_name, description, stars,
    language, owner, html_url
    """
    owner, repo = _parse_github_url(github_url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url, headers=_get_headers(), timeout=15)
    response.raise_for_status()

    data = response.json()
    return {
        "name": data.get("name", ""),
        "full_name": data.get("full_name", ""),
        "description": data.get("description", ""),
        "stars": data.get("stargazers_count", 0),
        "language": data.get("language", "Unknown"),
        "owner": data.get("owner", {}).get("login", ""),
        "html_url": data.get("html_url", ""),
        "topics": data.get("topics", []),
    }


def fetch_readme(github_url: str) -> str:
    """
    Fetch the README.md content from a GitHub repository.

    The GitHub API returns README content as base64-encoded text,
    which we decode to plain text. Returns empty string if no README found.
    """
    owner, repo = _parse_github_url(github_url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    response = requests.get(api_url, headers=_get_headers(), timeout=15)

    if response.status_code == 404:
        return "(No README found in this repository)"

    response.raise_for_status()

    data = response.json()
    content_b64 = data.get("content", "")

    # GitHub returns base64-encoded content — decode it
    try:
        readme_text = base64.b64decode(content_b64).decode("utf-8")
    except Exception:
        readme_text = "(Could not decode README content)"

    # Truncate very long READMEs to avoid exceeding token limits
    max_chars = 8000
    if len(readme_text) > max_chars:
        readme_text = readme_text[:max_chars] + "\n\n... (README truncated for brevity)"

    return readme_text
