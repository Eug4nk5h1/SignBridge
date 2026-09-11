import sys

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except ImportError:
    nlp = None

QUESTION_WORDS = ["who", "what", "where", "when", "why", "how"]


def analyze_sentence(sentence):
    result = {
        "sentence_type": "STATEMENT",
        "question_type": None,
        "subject": None,
        "verb": None,
        "object": None,
        "location": None,
        "time": None
    }

    if sentence.strip().endswith("?"):
        result["sentence_type"] = "QUESTION"

    if nlp is not None:
        doc = nlp(sentence)

        for token in doc:
            if token.text.lower() in QUESTION_WORDS:
                result["question_type"] = token.text.upper()

            if token.dep_ == "nsubj":
                result["subject"] = token.text.upper()

            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                result["verb"] = token.lemma_.upper()

            if token.dep_ == "dobj":
                result["object"] = token.text.upper()

            if token.dep_ == "pobj":
                result["location"] = token.text.upper()

            if token.ent_type_ in ["TIME", "DATE"]:
                result["time"] = token.text.upper()
    else:
        # Fallback token extraction when spacy model is not installed
        words = [w.strip(".,!?").upper() for w in sentence.split()]
        for w in words:
            if w.lower() in QUESTION_WORDS:
                result["question_type"] = w
            elif w in ["I", "YOU", "HE", "SHE", "THEY", "ME", "BROTHER", "SISTER", "PLEASE"]:
                if not result["subject"]:
                    result["subject"] = w
            elif w in ["GO", "GOING", "EAT", "DRINK", "READ", "WRITE", "HELP", "COME", "SIT", "STAND", "STOP"]:
                if not result["verb"]:
                    result["verb"] = w
            elif w in ["WATER", "FOOD", "TEA", "BOOK"]:
                if not result["object"]:
                    result["object"] = w
            elif w in ["HOME", "HOSPITAL", "MARKET", "SCHOOL", "COLLEGE"]:
                if not result["location"]:
                    result["location"] = w
            elif w in ["TODAY", "TOMORROW"]:
                if not result["time"]:
                    result["time"] = w

    return result