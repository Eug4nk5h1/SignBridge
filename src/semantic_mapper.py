"""Context-aware English concept candidates for the controlled sign catalog.

Exact catalog matches remain deterministic. When an English expression is not
in the catalog, WordNet can suggest a candidate only when its context-selected
sense shares a synset with a catalog English form. A synonym is never accepted
from string similarity alone. Missing WordNet data, ambiguous senses, and
unsupported concepts stay visible as unresolved items.
"""

import json
import re
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "sign_catalog.json"
_CATALOG = None
_CATALOG_MTIME_NS = None
_GLOSS_ENTRIES = {}


def _normalize_form(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


_ALIAS_ENTRIES = defaultdict(set)
_PHRASE_ALIAS_ENTRIES = defaultdict(set)
_ORDERED_PHRASE_ALIASES = []


def _refresh_catalog_if_changed():
    """Reload catalog data and derived aliases after an on-disk catalog edit."""
    global _CATALOG, _CATALOG_MTIME_NS, _GLOSS_ENTRIES
    global _ALIAS_ENTRIES, _PHRASE_ALIAS_ENTRIES, _ORDERED_PHRASE_ALIASES

    modified_ns = CATALOG_PATH.stat().st_mtime_ns
    if modified_ns == _CATALOG_MTIME_NS:
        return

    with CATALOG_PATH.open(encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)
    gloss_entries = {
        (entry["language"], entry["gloss"].upper()): entry
        for entry in catalog["entries"]
    }
    aliases = defaultdict(set)
    phrase_aliases = defaultdict(set)
    for entry in catalog["entries"]:
        for form in entry.get("english_forms", []):
            normalized_form = _normalize_form(form)
            entry_key = (entry["language"], entry["gloss"].upper())
            form_words = tuple(normalized_form.split())
            if len(form_words) > 1:
                phrase_aliases[form_words].add(entry_key)
            else:
                aliases[normalized_form].add(entry_key)

    _CATALOG = catalog
    _GLOSS_ENTRIES = gloss_entries
    _ALIAS_ENTRIES = aliases
    _PHRASE_ALIAS_ENTRIES = phrase_aliases
    _ORDERED_PHRASE_ALIASES = sorted(
        phrase_aliases.items(), key=lambda item: len(item[0]), reverse=True
    )
    _CATALOG_MTIME_NS = modified_ns


def _collapse_catalog_phrases(tokens, target_language):
    """Collapse catalog phrases before mapping, including joined compound input."""
    collapsed = []
    index = 0
    while index < len(tokens):
        matched = None
        for phrase, entries in _ORDERED_PHRASE_ALIASES:
            phrase_tokens = tokens[index:index + len(phrase)]
            joined_phrase = re.sub(r"[\s-]+", "", " ".join(phrase))
            candidates = sorted(
                gloss for language, gloss in entries if language == target_language
            )
            exact_phrase_tokens = []
            if len(phrase_tokens) == len(phrase):
                token_words = tuple(
                    _normalize_form(token.get("lemma") or token.get("surface"))
                    for token in phrase_tokens
                )
                if token_words == phrase:
                    exact_phrase_tokens = phrase_tokens

            single_token = tokens[index]
            single_word = _normalize_form(single_token.get("lemma") or single_token.get("surface"))
            joined_form = re.sub(r"[\s-]+", "", single_word)
            joined_match = (
                len(phrase) > 1
                and len(joined_phrase) >= 7
                and joined_form == joined_phrase
            )
            if (exact_phrase_tokens or joined_match) and len(candidates) == 1:
                matched = (exact_phrase_tokens or [single_token], candidates[0])
                break

        if matched:
            phrase_tokens, gloss = matched
            collapsed.append({
                **phrase_tokens[0],
                "surface": " ".join(str(token.get("surface") or "") for token in phrase_tokens),
                "lemma": " ".join(phrase),
                "candidate_gloss": gloss,
                "catalog_phrase": True,
            })
            index += len(phrase_tokens)
        else:
            collapsed.append(tokens[index])
            index += 1
    return collapsed


@lru_cache(maxsize=1)
def _wordnet_modules():
    """Return WordNet tools when both the Python package and corpus are installed."""
    try:
        from nltk.corpus import wordnet as wn
        # Force lazy corpus loading here so a missing corpus is reported cleanly.
        wn.synsets("sign")
        return wn
    except (ImportError, LookupError):
        return None


def _wordnet_pos(spacy_pos):
    return {
        "NOUN": "n",
        "PROPN": "n",
        "VERB": "v",
        "ADJ": "a",
        "ADV": "r",
    }.get(spacy_pos)


def _entry_synsets(wn, entry, pos):
    synsets = set()
    for form in entry.get("english_forms", []):
        lookup = _normalize_form(form).replace(" ", "_")
        synsets.update(wn.synsets(lookup, pos=pos))
    return synsets


def _signature_overlap(synset, context_words):
    signature = set()
    signature_text = [synset.definition(), *synset.examples()]
    signature_text.extend(lemma.name().replace("_", " ") for lemma in synset.lemmas())
    for text in signature_text:
        signature.update(re.findall(r"[a-z]+", text.lower()))
    return len(signature & context_words)


def _wordnet_candidate(token, analysis, target_language, wn):
    lemma = _normalize_form(token.get("lemma") or token.get("surface"))
    pos = _wordnet_pos(token.get("pos"))
    if not lemma or not pos:
        return None, [], "WordNet has no matching part of speech for this token.", None

    query_synsets = wn.synsets(lemma.replace(" ", "_"), pos=pos)
    if not query_synsets:
        return None, [], "No WordNet sense was found for this expression.", None

    senses_by_gloss = defaultdict(set)
    for (language, gloss), entry in _GLOSS_ENTRIES.items():
        if language != target_language:
            continue
        for synset in _entry_synsets(wn, entry, pos):
            if synset in query_synsets:
                senses_by_gloss[gloss].add(synset)

    candidate_glosses = sorted(senses_by_gloss)
    if not candidate_glosses:
        return None, [], "No catalog concept shares a WordNet sense with this expression.", None

    mapped_senses = {
        synset: [gloss for gloss in candidate_glosses if synset in senses_by_gloss[gloss]]
        for synset in query_synsets
    }
    context = [
        _normalize_form(word)
        for word in analysis.get("context_words", [])
        if _normalize_form(word)
    ]
    context_words = {
        word
        for item in context
        for word in re.findall(r"[a-z]+", item)
        if word != lemma
    }

    if len(query_synsets) == 1:
        only_sense = query_synsets[0]
        only_glosses = mapped_senses.get(only_sense, [])
        if len(only_glosses) == 1:
            return only_glosses[0], candidate_glosses, None, 0.88

    scored_senses = [
        (_signature_overlap(sense, context_words), sense)
        for sense in query_synsets
    ]
    best_score = max((score for score, _ in scored_senses), default=0)
    best_senses = [sense for score, sense in scored_senses if score == best_score]
    best_mappings = [set(mapped_senses.get(sense, [])) for sense in best_senses]
    selected_glosses = set.union(*best_mappings) if best_mappings else set()
    all_best_senses_support_candidate = all(len(items) == 1 for items in best_mappings)
    if best_score > 0 and all_best_senses_support_candidate and len(selected_glosses) == 1:
        return next(iter(selected_glosses)), candidate_glosses, None, 0.78
    if candidate_glosses:
        return None, candidate_glosses, "Context did not select one suitable catalog concept.", None
    return None, [], "No context-resolved catalog concept was found.", None


def resolve_semantic_sequence(analysis, target_language="ASL"):
    """Resolve normalized tokens to catalog glosses, retaining unresolved words.

    The return value includes both the sequence used by target-language rules
    and an auditable per-token trace showing exact, WordNet, or unresolved
    decisions.
    """
    _refresh_catalog_if_changed()
    wn = _wordnet_modules()
    tokens = analysis.get("semantic_tokens") or [
        {"surface": word, "lemma": str(word).lower(), "pos": "X", "candidate_gloss": word}
        for word in analysis.get("keywords", [])
    ]
    tokens = _collapse_catalog_phrases(tokens, target_language)
    sequence = []
    trace = []

    for token in tokens:
        surface = str(token.get("surface") or token.get("lemma") or "")
        lemma = _normalize_form(token.get("lemma") or surface)
        candidate = str(token.get("candidate_gloss") or lemma).strip().upper()
        gloss_entry = _GLOSS_ENTRIES.get((target_language, candidate))

        if gloss_entry:
            resolved = candidate
            status = "resolved"
            method = "catalog_english_phrase" if token.get("catalog_phrase") else "exact_gloss"
            possible = [candidate]
            reason = (
                "The expression matches one curated target-language catalog phrase."
                if token.get("catalog_phrase")
                else "The normalized gloss is present in the target-language catalog."
            )
            confidence = 1.0
        else:
            exact_aliases = sorted(
                gloss
                for language, gloss in _ALIAS_ENTRIES.get(lemma, set())
                if language == target_language
            )
            if len(exact_aliases) == 1:
                resolved = exact_aliases[0]
                status = "resolved"
                method = "catalog_english_form"
                possible = exact_aliases
                reason = "The expression matches a curated English form in the catalog."
                confidence = 0.98
            elif len(exact_aliases) > 1:
                resolved = None
                status = "ambiguous"
                method = "catalog_english_form"
                possible = exact_aliases
                reason = "The expression matches more than one catalog concept."
                confidence = None
            elif wn is not None:
                resolved, possible, reason, confidence = _wordnet_candidate(
                    token, analysis, target_language, wn
                )
                status = "resolved" if resolved else "unresolved"
                method = "wordnet_context" if resolved else "wordnet_candidate_review"
            else:
                resolved = None
                possible = []
                status = "unresolved"
                method = "catalog_only"
                reason = "WordNet is not installed with its corpus; no exact catalog match exists."
                confidence = None

        sequence.append(resolved or candidate)
        trace.append({
            "input": surface,
            "normalized": lemma,
            "candidate_gloss": candidate,
            "resolved_gloss": resolved,
            "candidate_concepts": possible,
            "method": method,
            "confidence": confidence,
            "status": status,
            "reason": reason,
        })

    return {
        "sequence": sequence,
        "trace": trace,
        "semantic_resource": "WordNet" if wn is not None else "curated catalog only",
    }
