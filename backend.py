from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.speech import speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl
from src.sign_library import get_absolute_sign_path


app = FastAPI(title="SignBridge AI Backend")


# Allow React to communicate with Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporary audio storage
TEMP_DIR = Path("temp_audio")
TEMP_DIR.mkdir(exist_ok=True)


# Make ASL videos available to React
app.mount(
    "/signs",
    StaticFiles(directory="assets/signs"),
    name="signs"
)


@app.get("/")
def home():
    return {
        "message": "SignBridge AI backend is running"
    }


@app.post("/translate")
async def translate(file: UploadFile = File(...)):

    audio_path = TEMP_DIR / "recording.webm"

    # Save microphone recording
    with audio_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Speech → Text
    text = speech_to_text(str(audio_path))

    # Text → linguistic analysis
    analysis = analyze_sentence(text)

    # Linguistic analysis → ASL sequence
    sign_sequence = translate_to_asl(analysis)

    # Find corresponding sign videos
    signs = []

    for sign in sign_sequence:

        video_path = get_absolute_sign_path(sign)

        signs.append({
            "word": sign,
            "video": (
                f"/signs/{Path(video_path).name}"
                if video_path
                else None
            ),
            "found": video_path is not None
        })

    return {
        "text": text,
        "analysis": analysis,
        "sign_sequence": sign_sequence,
        "signs": signs
    }