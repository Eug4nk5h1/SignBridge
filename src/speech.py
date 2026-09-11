import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper


# FFmpeg path
os.environ["PATH"] += os.pathsep + r"C:\Users\eugan\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.GPL_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-N-125875-g5d4d3bdc61-win64-gpl\bin"


SAMPLE_RATE = 16000
DURATION = 5
AUDIO_FILE = "input.wav"


def record_audio():
    """Record audio from the microphone."""

    print("🎤 Speak now...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()

    write(AUDIO_FILE, SAMPLE_RATE, audio)

    print("Recording completed.")

    return AUDIO_FILE


def speech_to_text(audio_file):
    """Convert recorded speech into English text using Whisper."""

    print("Loading Whisper...")

    model = whisper.load_model("base")

    result = model.transcribe(audio_file)

    text = result["text"].strip()

    return text