/**
 * RepoInput Component
 *
 * Provides a GitHub URL input field with an "Analyze" button.
 * Calls the backend /analyze-with-context endpoint and passes
 * the analysis results up to the parent component.
 */

import { useState } from 'react';

const API_BASE = 'http://localhost:8000';

export default function RepoInput({ onAnalyzed, setLoading, setError }) {
  const [url, setUrl] = useState('');

  /**
   * Handle the analyze button click.
   * Sends GitHub URL to backend and processes the response.
   */
  const handleAnalyze = async () => {
    // Validate URL
    if (!url.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    if (!url.includes('github.com')) {
      setError('Please enter a valid GitHub URL (e.g., https://github.com/owner/repo)');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/analyze-with-context`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ github_url: url.trim() }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      onAnalyzed(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze repository. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Allow pressing Enter to submit.
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  return (
    <div className="repo-input-section glass-card">
      <div className="input-group">
        <input
          id="github-url-input"
          type="url"
          placeholder="https://github.com/username/repository"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="GitHub repository URL"
        />
        <button
          id="analyze-btn"
          className="btn-primary"
          onClick={handleAnalyze}
          aria-label="Analyze repository"
        >
          🔍 Analyze
        </button>
      </div>
    </div>
  );
}
