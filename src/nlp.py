import spacy

nlp = spacy.load("en_core_web_sm")

QUESTION_WORDS = ["who", "what", "where", "when", "why", "how"]


def analyze_sentence(sentence):
    doc = nlp(sentence)

    result = {
        "sentence_type": "STATEMENT",
        "question_type": None,
        "subject": None,
        "verb": None,
        "object": None,
        "location": None,
        "time": None
    }

    # Detect question
    if sentence.strip().endswith("?"):
        result["sentence_type"] = "QUESTION"

    for token in doc:

        # Question word
        if token.text.lower() in QUESTION_WORDS:
            result["question_type"] = token.text.upper()

        # Subject
        if token.dep_ == "nsubj":
            result["subject"] = token.text.upper()

        # Main verb
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            result["verb"] = token.lemma_.upper()

        # Direct object
        if token.dep_ == "dobj":
            result["object"] = token.text.upper()

        # Location / object of preposition
        if token.dep_ == "pobj":
            result["location"] = token.text.upper()

        # Time expressions
        if token.ent_type_ == "TIME" or token.ent_type_ == "DATE":
            result["time"] = token.text.upper()

    return result