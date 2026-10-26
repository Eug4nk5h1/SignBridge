from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.nlp import analyze_sentence
from src.sign_library import PROJECT_ROOT, get_absolute_sign_path
from src.speech import speech_to_text
from src.translator import translate_to_asl

app = FastAPI(title="SignBridge AI Backend")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
TEMP_DIR = PROJECT_ROOT / "temp_audio"
TEMP_DIR.mkdir(exist_ok=True)
SIGNS_DIR = PROJECT_ROOT / "assets" / "signs"
app.mount("/signs", StaticFiles(directory=str(SIGNS_DIR)), name="signs")


@app.get("/")
def home():
    return {"message": "SignBridge AI backend is running"}


@app.post("/translate")
async def translate(file: UploadFile = File(...)):
    suffix = Path(file.filename or "recording.webm").suffix or ".webm"
    audio_path = None
    try:
        with NamedTemporaryFile(mode="wb", suffix=suffix, prefix="upload-", dir=TEMP_DIR, delete=False) as buffer:
            audio_path = Path(buffer.name)
            shutil.copyfileobj(file.file, buffer)
        text = speech_to_text(str(audio_path))
        analysis = analyze_sentence(text)
        sign_sequence = translate_to_asl(analysis)
        signs = []
        for sign in sign_sequence:
            video_path = get_absolute_sign_path(sign)
            signs.append({"word": sign, "video": f"/signs/{Path(video_path).name}" if video_path else None, "found": video_path is not None})
        return {"text": text, "analysis": analysis, "sign_sequence": sign_sequence, "signs": signs}
    finally:
        if audio_path is not None:
            audio_path.unlink(missing_ok=True)
