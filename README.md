# SignBridge AI

SignBridge is a controlled-vocabulary speech-to-sign prototype. It records/transcribes English, applies basic token and lexical rules, and presents available sign videos. It is not a complete ASL grammar translator; semantic synonym resolution and multilingual concept/sign identifiers remain proposed extensions.

## macOS setup

Requires Python 3.10–3.12, Node.js, and FFmpeg. Install FFmpeg with `brew install ffmpeg` and ensure `ffmpeg` is on your PATH. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn backend:app --reload
```

In a second terminal, run `cd frontend && npm install && npm run dev`. The desktop wrapper can be started in another terminal with `cd frontend && npm run electron` while Vite is running.

The first Whisper run downloads the selected model (`base` by default); set `SIGNBRIDGE_WHISPER_MODEL` to `tiny`, `small`, or another Whisper model name to change it. Allow microphone access when prompted.

## Supported behavior

The rules normalize common possessives (`my` → `I`, `your` → `YOU`), verb inflections through spaCy lemmatization, omit basic forms of `be` where appropriate, preserve negation, retain question words, append `QUESTION` for yes/no questions, and return unresolved vocabulary so the interface can report missing clips. This is a prototype gloss sequence, not validated ASL translation.
