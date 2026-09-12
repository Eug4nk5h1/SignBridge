import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

QUESTION_WORDS = [
    "who",
    "what",
    "where",
    "when",
    "why",
    "how"
]


def analyze_sentence(sentence):
    """
    Analyze an English sentence and return
    structured linguistic information.
    """

    doc = nlp(sentence)

    result = {
        "sentence_type": "STATEMENT",
        "question_type": None,
        "subject": None,
        "verb": None,
        "object": None,
        "location": None,
        "time": None,
        "keywords": []
    }


    if sentence.strip().endswith("?"):
        result["sentence_type"] = "QUESTION"


    for token in doc:

        # Ignore punctuation
        if token.is_punct:
            continue

        # Ignore auxiliary verbs and common grammatical words
        if token.is_stop and token.text.lower() not in [
            "i", "you", "he", "she", "we", "they"
        ]:
            continue

        # Use lemma for verbs, original form for other words
        if token.pos_ == "VERB":
            word = token.lemma_.upper()
        else:
            word = token.text.upper()

        result["keywords"].append(word)


    for token in doc:

        if token.text.lower() in QUESTION_WORDS:
            result["question_type"] = token.text.upper()

        if token.dep_ in ["nsubj", "nsubjpass"]:
            result["subject"] = token.text.upper()

        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            result["verb"] = token.lemma_.upper()

        if token.dep_ in ["dobj", "obj"]:
            result["object"] = token.text.upper()

        if token.dep_ == "pobj":
            result["location"] = token.text.upper()

        if token.ent_type_ in ["TIME", "DATE"]:
            result["time"] = token.text.upper()

    return result
