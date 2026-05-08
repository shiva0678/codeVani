/**
 * App.jsx — Main application component for CodeVani Lite
 *
 * Orchestrates the three main features:
 *   1. GitHub repo analysis (RepoInput)
 *   2. AI chat with translation (ChatBox + LanguageSelector)
 *   3. Loading/error states
 */

import { useState } from 'react';
import RepoInput from './components/RepoInput';
import ChatBox from './components/ChatBox';
import LanguageSelector from './components/LanguageSelector';
import './index.css';

export default function App() {
  // State for repo analysis results
  const [repoData, setRepoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('en');

  /** Called when repo analysis completes successfully */
  const handleAnalyzed = (data) => {
    setRepoData(data);
    setError(null);
  };

  return (
    <div className="app-container">
      {/* ── Header ──────────────────────────────── */}
      <header className="app-header">
        <span className="emoji-icon">🎙️</span>
        <h1>CodeVani Lite</h1>
        <p className="subtitle">
          AI-Powered GitHub Repo Analyzer · Chat · Translate · Listen
        </p>
      </header>

      {/* ── GitHub URL Input ────────────────────── */}
      <RepoInput
        onAnalyzed={handleAnalyzed}
        setLoading={setLoading}
        setError={setError}
      />

      {/* ── Error Banner ────────────────────────── */}
      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {/* ── Loading State ───────────────────────── */}
      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <div className="loading-text">Analyzing repository with AI...</div>
        </div>
      )}

      {/* ── Repo Summary ────────────────────────── */}
      {repoData && !loading && (
        <div className="repo-summary glass-card">
          <h2>📦 {repoData.repo_name}</h2>

          <div className="repo-meta">
            <span className="meta-badge">⭐ {repoData.stars}</span>
            <span className="meta-badge">💻 {repoData.language}</span>
          </div>

          <div className="summary-section">
            <h3>📝 Summary</h3>
            <div className="content">{repoData.summary}</div>
          </div>

          <div className="summary-section">
            <h3>🛠️ Tech Stack</h3>
            <div className="content">{repoData.tech_stack}</div>
          </div>

          <div className="summary-section">
            <h3>🚀 Setup Instructions</h3>
            <div className="content">{repoData.setup_instructions}</div>
          </div>
        </div>
      )}

      {/* ── Chat Interface (visible after analysis) ── */}
      {repoData && !loading && (
        <>
          <LanguageSelector language={language} setLanguage={setLanguage} />
          <ChatBox language={language} />
        </>
      )}

      {/* ── Welcome State (before analysis) ──────── */}
      {!repoData && !loading && !error && (
        <div className="welcome-state">
          <div className="icon">🚀</div>
          <h3>Welcome to CodeVani Lite</h3>
          <p>Enter a GitHub repository URL above to get started</p>
        </div>
      )}

      {/* ── Footer ──────────────────────────────── */}
      <footer className="app-footer">
        CodeVani Lite · Built with ❤️ · React + FastAPI + Gemini AI
      </footer>
    </div>
  );
}
