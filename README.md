# SignBridge AI

SignBridge is a speech-to-sign **prototype** for demonstrating a controlled English-to-ASL-gloss pipeline. It records spoken English, transcribes it with Whisper, analyzes tokens with spaCy, applies a curated lexicon and rules, maps each gloss to a project-local concept ID and ASL sign ID, checks for a local sign video, and plays available clips in sequence.

It does not translate arbitrary English into fluent ASL. The gloss rules are limited, the catalog covers a small vocabulary, and some words may have no clip. Concept and sign IDs are identifiers created for this project; they are not official ASL standards. Read [the architecture and scope](docs/ARCHITECTURE.md) before describing the project.

## What the prototype demonstrates

- Audio capture in the React interface and speech transcription by OpenAI Whisper.
- spaCy-based token analysis, lemmatization, and basic question detection.
- Curated mappings for supported pronouns, inflections, negation, questions, and phrases.
- Exact catalog matching plus cautious WordNet synonym candidates selected using surrounding context; ambiguous or unsupported words remain unresolved.
- An expanded 84-entry local catalog, including the additional individual signs and supported phrase clips copied from the user's Signbank downloads.
- An explicit gloss → concept ID → language-specific sign ID lookup in `data/sign_catalog.json`.
- Video availability checks and sequential playback; missing clips are reported in the interface.
- A demo phrase such as “Where is your friend going?” should yield the curated sequence `WHERE YOU FRIEND GO`.

## Requirements

- macOS, Python 3.10–3.12, Node.js 20.19+ or 22.12+, Git, and FFmpeg.
- Microphone permission in the browser.
- Internet for the first Whisper model download. Transcription runs locally after download.
- Git LFS to fetch the sign videos.

Install FFmpeg and Git LFS with Homebrew:

```sh
brew install ffmpeg git-lfs
git lfs install
```

Clone the repository, then fetch its video assets:

```sh
git lfs pull
```

## Setup

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader wordnet
npm --prefix frontend ci
```

The WordNet download enables context-based synonym candidates. If WordNet is
not installed, exact catalog matches still work and unfamiliar expressions
remain unresolved instead of being guessed.

The first transcription downloads Whisper’s `base` model. Set `SIGNBRIDGE_WHISPER_MODEL=tiny` for a faster, less accurate demo or choose another installed Whisper model.

## Run

Open two terminal windows from the repository root. In the first:

```sh
source .venv/bin/activate
python -m uvicorn backend:app --reload
```

In the second:

```sh
npm --prefix frontend run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`) and allow microphone access. The backend health endpoint is `http://127.0.0.1:8000/`.

## Checks

```sh
source .venv/bin/activate
python -m unittest discover -s tests -v
npm --prefix frontend run lint
npm --prefix frontend run build
```

See [the professor demo guide](docs/PROFESSOR_DEMO.md) for a short walkthrough and expected observations.

## Repository map

- `backend.py` — API endpoint and end-to-end request orchestration.
- `src/speech.py` — Whisper transcription.
- `src/nlp.py` — token and sentence analysis.
- `src/semantic_mapper.py` — exact lexical matching, context-based WordNet candidates, and a per-token decision trace.
- `src/translator.py` — curated English-analysis-to-gloss rules and supported phrase clips such as **best friend**, **don't know**, **don't like**, and **what's up**.
- `src/concept_mapper.py` — catalog lookup, IDs, and resource checks.
- `data/sign_catalog.json` — project concept/sign records and clip filenames.
- `assets/signs/` — Git LFS-backed video resources.
- `docs/ADDING_SIGN_VIDEOS.md` — exact steps for replacing clips and recording their sources and licenses.
- `frontend/` — three-stage web interface and sequential video playback.
- `tests/` — automated checks of the documented prototype behavior.
