"""
Text-to-Speech Service — Converts text to audio using gTTS.

Generates MP3 audio files from text in the appropriate language
and returns a URL path for the frontend to play.
"""

import os
import uuid
from gtts import gTTS

# Directory to store generated audio files
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_files")

# Ensure audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Map our language codes to gTTS language codes
GTTS_LANG_MAP = {
    "en": "en",
    "hi": "hi",
    "kn": "kn",
}


def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Convert text to an MP3 audio file.

    Args:
        text: The text to convert to speech
        lang: Language code ('en', 'hi', 'kn')

    Returns:
        The filename of the generated audio file (not full path).
        Frontend can access it via /audio/{filename}
    """
    # Use gTTS-compatible language code
    gtts_lang = GTTS_LANG_MAP.get(lang, "en")

    # Generate a unique filename to avoid collisions
    filename = f"tts_{uuid.uuid4().hex[:10]}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(filepath)
        return filename
    except Exception as e:
        print(f"[TTS Error] Failed to generate speech: {e}")
        raise


def cleanup_old_files(max_files: int = 50):
    """
    Remove oldest audio files if we exceed max_files.
    Prevents disk space issues during long sessions.
    """
    files = sorted(
        [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR)],
        key=os.path.getmtime,
    )
    while len(files) > max_files:
        os.remove(files.pop(0))
