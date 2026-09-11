import spacy

nlp = spacy.load("en_core_web_sm")


def classify_sentence(sentence):
    doc = nlp(sentence)

    # Check whether the sentence is a question
    if sentence.strip().endswith("?"):
        sentence_type = "QUESTION"
    else:
        sentence_type = "STATEMENT"

    question_word = None

    # Look for common question words
    question_words = ["who", "what", "where", "when", "why", "how"]

    for token in doc:
        if token.text.lower() in question_words:
            question_word = token.text.lower()
            break

    return sentence_type, question_word


# Test
sentences = [
    "I am going to college.",
    "Where are you going?",
    "What are you doing?",
    "Who is your teacher?",
    "When are you coming?"
]

for sentence in sentences:
    sentence_type, question_word = classify_sentence(sentence)

    print("\nSentence:", sentence)
    print("Type:", sentence_type)
    print("Question word:", question_word)