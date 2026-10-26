"""Resolve ASL glosses to local concept/sign records and video resources."""

import json
from pathlib import Path

from src.sign_library import SIGNS_FOLDER

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "sign_catalog.json"
with CATALOG_PATH.open(encoding="utf-8") as catalog_file:
    _catalog = json.load(catalog_file)

_ENTRIES = {
    (entry["language"], entry["gloss"].upper()): entry
    for entry in _catalog["entries"]
}


def resolve_sign_sequence(gloss_sequence, target_language="ASL"):
    """Return ordered concept/sign metadata, including explicit unresolved states."""
    results = []
    for raw_gloss in gloss_sequence:
        gloss = str(raw_gloss).strip().upper()
        entry = _ENTRIES.get((target_language, gloss))
        if entry is None:
            results.append({
                "word": gloss,
                "gloss": gloss,
                "concept_id": None,
                "concept_label": None,
                "sign_id": None,
                "language": target_language,
                "video": None,
                "found": False,
                "status": "unresolved",
                "message": "No curated concept/sign mapping is available.",
            })
            continue

        video_path = SIGNS_FOLDER / entry["video_file"]
        exists = video_path.is_file()
        results.append({
            "word": gloss,
            "gloss": gloss,
            "concept_id": entry["concept_id"],
            "concept_label": entry["concept_label"],
            "sign_id": entry["sign_id"],
            "language": target_language,
            "video": f"/signs/{entry['video_file']}" if exists else None,
            "found": exists,
            "status": "resolved" if exists else "resource_missing",
            "message": "Video available" if exists else "Mapped sign video is missing.",
        })
    return results


def catalog_summary():
    """Return public counts for the demo and project documentation."""
    languages = sorted({entry["language"] for entry in _catalog["entries"]})
    return {"concept_count": len(_catalog["entries"]), "languages": languages}
