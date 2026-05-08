"""
Translation Service — Translates text between languages.

Uses the deep-translator library (Google Translate wrapper)
to translate AI responses into Hindi and Kannada.

Supported languages:
  - 'en' — English (default, no translation needed)
  - 'hi' — Hindi
  - 'kn' — Kannada
"""

from deep_translator import GoogleTranslator

# Supported target languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
}


def translate_text(text: str, target_lang: str) -> str:
    """
    Translate text to the target language.

    Args:
        text: The English text to translate
        target_lang: Language code ('en', 'hi', 'kn')

    Returns:
        Translated text string. Returns original text if target is English
        or if translation fails.
    """
    # No translation needed for English
    if target_lang == "en":
        return text

    # Validate language code
    if target_lang not in SUPPORTED_LANGUAGES:
        return text

    try:
        # deep-translator has a 5000 char limit per request,
        # so we chunk long texts
        if len(text) > 4500:
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translated_chunks = []
            for chunk in chunks:
                result = GoogleTranslator(source='en', target=target_lang).translate(chunk)
                translated_chunks.append(result)
            return ''.join(translated_chunks)
        else:
            return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translation Error] Failed to translate to {target_lang}: {e}")
        # Return original text as fallback
        return text


def get_supported_languages() -> dict:
    """Return dict of supported language codes and their names."""
    return SUPPORTED_LANGUAGES
