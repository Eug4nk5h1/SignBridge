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
        "time": None
    }

    # ----------------------------------------
    # Sentence classification
    # ----------------------------------------

    if sentence.strip().endswith("?"):
        result["sentence_type"] = "QUESTION"

    # ----------------------------------------
    # Analyze individual tokens
    # ----------------------------------------

    for token in doc:

        # Question word
        if token.text.lower() in QUESTION_WORDS:
            result["question_type"] = token.text.upper()

        # Subject
        if token.dep_ in ["nsubj", "nsubjpass"]:
            result["subject"] = token.text.upper()

        # Main verb
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            result["verb"] = token.lemma_.upper()

        # Direct object
        if token.dep_ in ["dobj", "obj"]:
            result["object"] = token.text.upper()

        # Object of preposition
        if token.dep_ == "pobj":
            result["location"] = token.text.upper()

        # Time / date
        if token.ent_type_ in ["TIME", "DATE"]:
            result["time"] = token.text.upper()

    return result