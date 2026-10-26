import os
from functools import lru_cache
from pathlib import Path

import sounddevice as sd
import whisper
from scipy.io.wavfile import write

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_FILE = PROJECT_ROOT / "temp_audio" / "input.wav"
SAMPLE_RATE = 16000
DURATION = 5


@lru_cache(maxsize=1)
def _whisper_model():
    return whisper.load_model(os.getenv("SIGNBRIDGE_WHISPER_MODEL", "base"))


def record_audio():
    """Record a short microphone sample and return its absolute path."""
    AUDIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    print("🎤 Speak now...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    write(str(AUDIO_FILE), SAMPLE_RATE, audio)
    print("Recording completed.")
    return str(AUDIO_FILE)


def speech_to_text(audio_file):
    """Transcribe audio with Whisper; FFmpeg must be installed and on PATH."""
    result = _whisper_model().transcribe(str(audio_file), language="en")
    return result["text"].strip()
