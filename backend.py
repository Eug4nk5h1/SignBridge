from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.concept_mapper import catalog_summary, resolve_sign_sequence
from src.nlp import analyze_sentence
from src.semantic_mapper import resolve_semantic_sequence
from src.sign_library import PROJECT_ROOT
from src.speech import speech_to_text
from src.translator import transform_to_target_language

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
        if not text:
            raise HTTPException(status_code=422, detail="No speech was recognized. Try again and speak clearly.")
        analysis = analyze_sentence(text)
        semantic_mapping = resolve_semantic_sequence(analysis, target_language="ASL")
        transformation = transform_to_target_language(
            analysis,
            semantic_mapping["sequence"],
            target_language="ASL",
        )
        sign_sequence = transformation["sequence"]
        signs = resolve_sign_sequence(sign_sequence)
        return {
            "text": text,
            "analysis": analysis,
            "sign_sequence": sign_sequence,
            "concept_sequence": [
                {"gloss": item["gloss"], "concept_id": item["concept_id"], "status": item["status"]}
                for item in signs
            ],
            "signs": signs,
            "catalog": catalog_summary(),
            "semantic_mapping": semantic_mapping,
            "target_transformation": transformation,
            "translation_method": (
                "whisper_spacy_wordnet_and_controlled_asl_rules"
                if semantic_mapping["semantic_resource"] == "WordNet"
                else "whisper_spacy_catalog_and_controlled_asl_rules"
            ),
        }
    finally:
        if audio_path is not None:
            audio_path.unlink(missing_ok=True)
