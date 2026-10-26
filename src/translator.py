"""Controlled English-to-ASL gloss transformation for the supported prototype."""

PHRASE_NORMALIZATIONS = {("GOOD", "BYE"): "GOODBYE"}
AUXILIARIES = {"BE"}


def translate_to_asl(analysis):
    """Transform analyzed tokens while retaining negation and unresolved words."""
    keywords = [str(word).upper() for word in analysis.get("keywords", []) if word]
    signs = []
    i = 0
    while i < len(keywords):
        if i + 1 < len(keywords) and (keywords[i], keywords[i + 1]) in PHRASE_NORMALIZATIONS:
            signs.append(PHRASE_NORMALIZATIONS[(keywords[i], keywords[i + 1])])
            i += 2
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
