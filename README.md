# 🎙️ CodeVani Lite

**AI-Powered GitHub Repository Analyzer** with Chat, Translation & Text-to-Speech

> Analyze any public GitHub repo, ask questions about it, get answers in **English**, **Hindi**, or **Kannada**, and listen to the response!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Repo Analysis** | Enter a GitHub URL → get AI-generated summary, tech stack, and setup instructions |
| 💬 **Chat System** | ChatGPT-style interface to ask questions about the analyzed repo |
| 🌐 **Translation** | Translate AI responses to Hindi (हिन्दी) or Kannada (ಕನ್ನಡ) |
| 🔊 **Text-to-Speech** | Listen to responses in your chosen language |

---

## 🧱 Tech Stack

- **Frontend:** React (Vite) + Custom CSS
- **Backend:** Python FastAPI
- **AI:** Google Gemini 1.5 Flash
- **Translation:** googletrans
- **TTS:** gTTS (Google Text-to-Speech)
- **GitHub API:** REST API for repo data

---

## 📁 Project Structure

```
CODE_VANI/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── routes/
│   │   ├── repo.py              # /analyze endpoint
│   │   └── chat.py              # /chat endpoint
│   └── services/
│       ├── github_service.py    # GitHub API integration
│       ├── ai_service.py        # Gemini AI integration
│       ├── translation_service.py  # Translation logic
│       └── tts_service.py       # Text-to-Speech logic
│
└── frontend/
    ├── index.html
    ├── package.json
    └── src/
        ├── main.jsx             # React entry point
        ├── App.jsx              # Main app component
        ├── index.css            # Premium dark theme
        └── components/
            ├── RepoInput.jsx    # GitHub URL input
            ├── ChatBox.jsx      # Chat interface
            └── LanguageSelector.jsx  # Language dropdown
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **Google Gemini API Key** (free at https://aistudio.google.com/apikey)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_key_here

# Start the server
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 3. Open the App

Open **http://localhost:5173** in your browser.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key |
| `GITHUB_TOKEN` | ❌ Optional | GitHub PAT for higher rate limits |

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze-with-context` | Analyze a GitHub repo |
| POST | `/chat` | Ask a question about the repo |
| GET | `/audio/{filename}` | Serve generated audio files |

---

## 🎯 How It Works

1. **User enters a GitHub URL** → Frontend sends it to `/analyze-with-context`
2. **Backend fetches repo data** → GitHub API returns metadata + README
3. **AI generates summary** → Gemini analyzes and creates structured summary
4. **User asks questions** → Questions go to `/chat` with repo context
5. **Response is translated** → googletrans converts to Hindi/Kannada
6. **Audio is generated** → gTTS creates MP3, served via `/audio/` endpoint
7. **Frontend plays audio** → User can read and listen to the response

---

Built with ❤️ for hackathons
