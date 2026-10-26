
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# QUESTION WORDS
# --------------------------------------------------

QUESTION_WORDS = [
    "who",
    "what",
    "where",
    "when",
    "why",
    "how",
]


# --------------------------------------------------
# YES / NO QUESTION AUXILIARIES
# --------------------------------------------------

YES_NO_AUXILIARIES = [
    "is", "are", "am", "was", "were",
    "do", "does", "did",
    "can", "could", "will", "would",
    "shall", "should",
    "have", "has", "had",
    "may", "might", "must",
]


# --------------------------------------------------
# SUPPORTED SIGN VOCABULARY
# Video availability is checked separately when signs are returned.
# --------------------------------------------------

SIGN_VOCABULARY = {
    "bad", "college", "come", "drink", "eat",
    "family", "friend", "go", "good", "goodbye",
    "he", "hello", "help", "home", "how", "i",
    "know", "learn", "like", "love", "morning",
    "name", "need", "night", "no", "please",
    "school", "she", "sleep", "sorry", "student",
    "study", "teacher", "thank", "they", "today",
    "tomorrow", "understand", "want", "we",
    "welcome", "what", "when", "where", "who",
    "why", "work", "yes", "yesterday", "you",
}


# --------------------------------------------------
# ENGLISH -> AVAILABLE SIGN MAPPINGS
# --------------------------------------------------

WORD_MAPPINGS = {
    # Possessives
    "my": "MY",
    "mine": "I",
    "your": "YOUR",
    "yours": "YOU",
    "our": "WE",
    "their": "THEY",
    "his": "HIS",
    "her": "SHE",

    # Object pronouns
    "me": "ME",
    "him": "HE",
    "us": "WE",
    "them": "THEY",

    # Common verb forms
    "coming": "COME",
    "came": "COME",

    "going": "GO",
    "went": "GO",
    "gone": "GO",

    "eating": "EAT",
    "ate": "EAT",

    "drinking": "DRINK",
    "drank": "DRINK",

    "learning": "LEARN",
    "learned": "LEARN",

    "studying": "STUDY",
    "studied": "STUDY",

    "working": "WORK",
    "worked": "WORK",

    "sleeping": "SLEEP",
    "slept": "SLEEP",

    "helping": "HELP",
    "helped": "HELP",

    "knowing": "KNOW",
    "knew": "KNOW",

    "liking": "LIKE",
    "liked": "LIKE",

    "loving": "LOVE",
    "loved": "LOVE",

    "wanting": "WANT",
    "wanted": "WANT",

    "needing": "NEED",
    "needed": "NEED",

    "understanding": "UNDERSTAND",
    "understood": "UNDERSTAND",

    # Greetings
    "hi": "HELLO",
    "thanks": "THANK",
    "thankyou": "THANK",
    "thank": "THANK",

    # Time expressions
    "tonight": "NIGHT",
    "tonight's": "NIGHT",
    "yesterday": "YESTERDAY",
    "today": "TODAY",
    "tomorrow": "TOMORROW",

    # People and education
    "student": "STUDENT",
    "students": "STUDENT",
    "teachers": "TEACHER",
    "friends": "FRIEND",
    "families": "FAMILY",

    # Positive and negative
    "no": "NO",
    "not": "NO",
    "n't": "NO",
    "n’t": "NO",
    "'s": "BE",
    "’s": "BE",
    "cannot": "NO",
    "yes": "YES",

    # Common expressions
    "please": "PLEASE",
    "sorry": "SORRY",
    "welcome": "WELCOME",
}


# --------------------------------------------------
# WORDS THAT SHOULD NOT BECOME SIGNS
# --------------------------------------------------

SUPPORT_WORDS = {
    "a", "an", "the",
    "and", "or",
    "to", "of", "for",
    "in", "on", "at",
    "with", "from", "by",
    "be", "been", "being",
    "'s", "’s",
    "is", "are", "am",
    "was", "were",
    "do", "does", "did",
    "will", "would",
    "can", "could",
    "should", "shall",
    "have", "has", "had",
    "may", "might", "must",
}


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
        "keywords": [],
        "tokens": [],
        "semantic_tokens": [],
        "context_words": [],
    }

    # ==================================================
    # SENTENCE TYPE
    # ==================================================

    sentence_lower = sentence.strip().lower()

    # Explicit question mark
    if sentence_lower.endswith("?"):
        result["sentence_type"] = "QUESTION"

    # WH-question
    elif any(
        sentence_lower.startswith(word + " ")
        for word in QUESTION_WORDS
    ):
        result["sentence_type"] = "QUESTION"

    # Yes/No question
    elif any(
        sentence_lower.startswith(auxiliary + " ")
        for auxiliary in YES_NO_AUXILIARIES
    ):
        result["sentence_type"] = "QUESTION"

    # ==================================================
    # EXTRACT WORDS AND MAP TO AVAILABLE SIGNS
    # ==================================================

    for token in doc:

        # Ignore punctuation in the lexical sequence, but keep the grammatical
        # and semantic properties of every word for the later pipeline stages.
        if token.is_punct or token.is_space:
            continue

        original_word = token.text.lower()
        normalized_word = (
            token.lemma_.lower()
            if token.pos_ == "VERB"
            else original_word
        )
        token_info = {
            "surface": token.text,
            "lemma": normalized_word,
            "pos": token.pos_,
            "dependency": token.dep_,
            "head": token.head.lemma_.lower(),
            "entity_type": token.ent_type_ or None,
            "is_support_word": normalized_word in SUPPORT_WORDS,
        }
        result["tokens"].append(token_info)
        result["context_words"].append(normalized_word)

        if normalized_word in SUPPORT_WORDS:
            continue

        if normalized_word in QUESTION_WORDS:
            gloss_candidate = normalized_word.upper()
        elif normalized_word in WORD_MAPPINGS:
            gloss_candidate = WORD_MAPPINGS[normalized_word]
        else:
            # Preserve unknown content so semantic mapping can consider it and,
            # if no suitable concept exists, report it as unresolved.
            gloss_candidate = normalized_word.upper()

        result["keywords"].append(gloss_candidate)
        result["semantic_tokens"].append({
            **token_info,
            "candidate_gloss": gloss_candidate,
        })

    # ==================================================
    # SENTENCE STRUCTURE
    # ==================================================

    for token in doc:

        # Question type
        if token.text.lower() in QUESTION_WORDS:
            if result["sentence_type"] == "QUESTION":
                result["question_type"] = token.text.upper()

        # Subject
        if token.dep_ in ["nsubj", "nsubjpass"]:
            result["subject"] = token.text.upper()

        # Main verb
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            result["verb"] = token.lemma_.upper()

        # Object
        if token.dep_ in ["dobj", "obj"]:
            result["object"] = token.text.upper()

        # Location
        if token.dep_ == "pobj":
            result["location"] = token.text.upper()

        # Time/date
        if token.ent_type_ in ["TIME", "DATE"]:
            result["time"] = token.text.upper()

    return result
