"""
AI Service — Handles all interactions with Google Gemini API.

Provides two main functions:
  1. summarize_repo()  — Generate a structured summary of a GitHub repo
  2. answer_question() — Answer user questions using repo context
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the verified Flash model identifier
MODEL_NAME = "gemini-flash-latest"


def summarize_repo(repo_info: dict, readme_content: str) -> dict:
    """
    Generate a structured summary of a GitHub repository.

    Uses Gemini to analyze the repo metadata and README, then returns:
      - summary: A plain-English overview of the project
      - tech_stack: Technologies/frameworks used
      - setup_instructions: How to set up and run the project
    """
    prompt = f"""You are a helpful coding assistant. Analyze this GitHub repository and provide a structured summary.

**Repository:** {repo_info.get('full_name', 'Unknown')}
**Description:** {repo_info.get('description', 'No description')}
**Primary Language:** {repo_info.get('language', 'Unknown')}
**Stars:** {repo_info.get('stars', 0)}
**Topics:** {', '.join(repo_info.get('topics', []))}

**README Content:**
{readme_content}

---

Please provide your response in EXACTLY this format (use these exact headers):

## Summary
(Write a clear, concise 2-3 sentence summary of what this project does and who it's for)

## Tech Stack
(List the key technologies, frameworks, and tools used, as bullet points)

## Setup Instructions
(Provide step-by-step setup instructions based on the README. If the README doesn't have setup info, provide reasonable guesses based on the tech stack)
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    # Parse the structured response into sections
    response_text = response.text
    sections = _parse_sections(response_text)

    return {
        "summary": sections.get("Summary", response_text),
        "tech_stack": sections.get("Tech Stack", "Not identified"),
        "setup_instructions": sections.get("Setup Instructions", "Not available"),
        "raw": response_text,
    }


def answer_question(context: str, question: str) -> str:
    """
    Answer a user's question about a repository using AI.

    Args:
        context: The repo summary/README to use as context
        question: The user's question

    Returns:
        A clear, helpful answer string
    """
    prompt = f"""You are CodeVani, a friendly AI assistant that helps people understand GitHub repositories.

Given this repository context:
---
{context}
---

Answer the user's question in simple, clear terms. If the answer isn't in the context, say so honestly but try to be helpful.

User's question: {question}

Provide a helpful, concise answer:"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text


def _parse_sections(text: str) -> dict:
    """
    Parse markdown-style sections from AI response.
    Splits on '## Header' patterns and returns {header: content} dict.
    """
    sections = {}
    current_header = None
    current_content = []

    for line in text.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_header:
                sections[current_header] = "\n".join(current_content).strip()
            current_header = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_header:
        sections[current_header] = "\n".join(current_content).strip()

    return sections
