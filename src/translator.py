"""Controlled English-to-ASL gloss transformation for the supported prototype."""

PHRASE_NORMALIZATIONS = {
    ("GOOD", "BYE"): "GOODBYE",
    ("BEST", "FRIEND"): "BEST_FRIEND",
    ("ALL", "MORNING"): "ALL_MORNING",
    ("ALL", "DAY", "NIGHT"): "ALL_DAY_AND_NIGHT",
    ("I", "NO", "KNOW"): "DONT_KNOW",
    ("NO", "KNOW"): "DONT_KNOW",
    ("NO", "LIKE"): "DONT_LIKE",
    ("ONLY", "ME"): "ONLY_ME",
    ("WHAT", "UP"): "WHATS_UP",
}
_ORDERED_PHRASE_RULES = sorted(
    PHRASE_NORMALIZATIONS.items(), key=lambda item: len(item[0]), reverse=True
)
AUXILIARIES = {"BE"}


def translate_to_asl(analysis, semantic_sequence=None):
    """Apply the project's explicit, controlled ASL-gloss transformation rules."""
    source_sequence = semantic_sequence or analysis.get("keywords", [])
    keywords = [str(word).upper() for word in source_sequence if word]
    signs = []
    i = 0
    while i < len(keywords):
        matched_phrase = next(
            (
                (phrase, gloss)
                for phrase, gloss in _ORDERED_PHRASE_RULES
                if tuple(keywords[i:i + len(phrase)]) == phrase
            ),
            None,
        )
        if matched_phrase:
            phrase, gloss = matched_phrase
            signs.append(gloss)
            i += len(phrase)
            continue
        word = keywords[i]
        i += 1
        if word in AUXILIARIES:
            continue
        # Possessives are normalized by nlp.py; simple lexical variants are handled here too.
        if word in {"MINE"}:
            word = "I"
        elif word in {"YOURS"}:
            word = "YOU"
        signs.append(word)

    # The documented prototype marks yes/no questions explicitly. Wh-words already
    # express the question type and are retained in their input position.
    if analysis.get("sentence_type") == "QUESTION" and not analysis.get("question_type"):
        signs.append("QUESTION")
    return signs


def transform_to_target_language(analysis, semantic_sequence, target_language="ASL"):
    """Apply a named target-language rule set and report its current scope."""
    if target_language != "ASL":
        raise ValueError(f"No transformation rules are configured for {target_language}.")

    return {
        "sequence": translate_to_asl(analysis, semantic_sequence),
        "target_language": target_language,
        "rule_set": "controlled_asl_gloss_v1",
        "rules_applied": [
            "normalize supported English forms",
            "remove selected English auxiliaries",
            "normalize supported multiword expressions to one catalog gloss",
            "preserve negation and time glosses",
            "append QUESTION to yes/no questions",
        ],
        "limitations": [
            "preserves source order except for explicit phrase rules",
            "not validated as fluent ASL grammar",
        ],
    }
