# ASL Sign Library
# Each word is mapped to a visual sign resource.

SIGN_LIBRARY = {
    "I": "i",
    "YOU": "you",
    "GO": "go",
    "COLLEGE": "college",
    "WHERE": "where",
    "WHAT": "what",
    "WHO": "who",
    "WHEN": "when",
    "WHY": "why",
    "HOW": "how",
    "DO": "do",
    "BOOK": "book",
    "READ": "read",
    "SHE": "she",
    "HE": "he",
    "THEY": "they",
    "TOMORROW": "tomorrow"
}


def get_sign(sign_word):
    return SIGN_LIBRARY.get(sign_word.upper())