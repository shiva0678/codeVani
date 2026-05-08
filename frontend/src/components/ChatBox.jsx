/**
 * ChatBox Component
 * ChatGPT-style chat interface with message bubbles,
 * translation display, and audio playback.
 */

import { useState, useRef, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

const LANG_NAMES = { en: 'English', hi: 'Hindi', kn: 'Kannada' };

export default function ChatBox({ language }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    const question = input.trim();
    if (!question) return;

    // Add user message
    const userMsg = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, language }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Server error');
      }

      const data = await res.json();
      const botMsg = {
        role: 'assistant',
        content: data.answer,
        translated: language !== 'en' ? data.translated_answer : null,
        translatedLang: language !== 'en' ? LANG_NAMES[language] : null,
        audioUrl: data.audio_url ? `${API_BASE}${data.audio_url}` : null,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errorMsg = {
        role: 'assistant',
        content: `❌ Error: ${err.message}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const playAudio = (url) => {
    const audio = new Audio(url);
    audio.play().catch((e) => console.warn('Audio play failed:', e));
  };

  return (
    <div className="chat-section glass-card">
      {/* Messages area */}
      <div className="chat-messages">
        {messages.length === 0 && !isTyping && (
          <div className="welcome-state">
            <div className="icon">💬</div>
            <h3>Ask anything about the repo</h3>
            <p>Type a question below to get started</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div>{msg.content}</div>

            {/* Show translation if available */}
            {msg.translated && (
              <div className="translated">
                <div className="translated-label">
                  🌐 {msg.translatedLang}
                </div>
                <div>{msg.translated}</div>
              </div>
            )}

            {/* Audio play button */}
            {msg.audioUrl && (
              <div className="audio-player">
                <button
                  className="btn-audio"
                  onClick={() => playAudio(msg.audioUrl)}
                  title="Play audio"
                >
                  🔊
                </button>
                <audio controls src={msg.audioUrl} style={{ flex: 1, height: 32 }} />
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="chat-input-area">
        <input
          id="chat-input"
          type="text"
          placeholder="Ask a question about the repository..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isTyping}
        />
        <button
          id="send-btn"
          className="btn-primary"
          onClick={sendMessage}
          disabled={isTyping || !input.trim()}
        >
          Send ➤
        </button>
      </div>
    </div>
  );
}
