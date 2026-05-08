/**
 * LanguageSelector Component
 * Dropdown for picking response language: English, Hindi, or Kannada.
 */

export default function LanguageSelector({ language, setLanguage }) {
  return (
    <div className="language-selector">
      <label htmlFor="language-select">🌐 Response Language:</label>
      <select
        id="language-select"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
      >
        <option value="en">🇬🇧 English</option>
        <option value="hi">🇮🇳 Hindi (हिन्दी)</option>
        <option value="kn">🇮🇳 Kannada (ಕನ್ನಡ)</option>
      </select>
    </div>
  );
}
