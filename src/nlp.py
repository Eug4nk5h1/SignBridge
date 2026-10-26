import spacy

# Load the documented English pipeline once at startup.
nlp = spacy.load("en_core_web_sm")
QUESTION_WORDS = {"who", "what", "where", "when", "why", "how"}
KEEP_STOP_WORDS = {"i", "you", "he", "she", "we", "they", "my", "your", "his", "her", "our", "their", "not", "no", "never", "n't", "n’t", "cannot", "this", "that", "these", "those", *QUESTION_WORDS}


def analyze_sentence(sentence):
    """Return a compact linguistic analysis without dropping negation."""
    sentence = (sentence or "").strip()
    doc = nlp(sentence)
    question_type = next((t.text.upper() for t in doc if t.text.lower() in QUESTION_WORDS), None)
    is_question = sentence.endswith("?")

    keywords = []
    for token in doc:
        if token.is_punct or token.is_space:
            continue
        lower = token.text.lower()
        # Keep content words, pronouns, negation, and possessives for target rules.
        if token.is_stop and lower not in KEEP_STOP_WORDS and token.pos_ not in {"VERB", "AUX"}:
            continue
        if lower in {"n't", "n’t"}:
            word = "NOT"
        elif lower in {"my", "mine"}:
            word = "I"
        elif lower in {"your", "yours"}:
            word = "YOU"
        elif token.pos_ in {"VERB", "AUX"} and token.lemma_:
            word = token.lemma_.upper()
        else:
            word = token.text.upper()
        keywords.append(word)

    return {
        "sentence_type": "QUESTION" if is_question else "STATEMENT",
        "question_type": question_type,
        "subject": next((t.text.upper() for t in doc if t.dep_ in {"nsubj", "nsubjpass"}), None),
        "verb": next((t.lemma_.upper() for t in doc if t.dep_ == "ROOT" and t.pos_ == "VERB"), None),
        "object": next((t.text.upper() for t in doc if t.dep_ in {"dobj", "obj"}), None),
        "location": next((t.text.upper() for t in doc if t.dep_ == "pobj"), None),
        "time": next((t.text.upper() for t in doc if t.ent_type_ in {"TIME", "DATE"}), None),
        "keywords": keywords,
    }
