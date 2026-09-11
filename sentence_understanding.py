import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")


def understand_sentence(sentence):
    doc = nlp(sentence)

    subject = None
    action = None
    destination = None

    for token in doc:

        # Find the subject
        if token.dep_ == "nsubj":
            subject = token.text

        # Find the main action
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            action = token.lemma_

        # Find a destination/object connected to a preposition
        if token.dep_ == "pobj":
            destination = token.text

    return subject, action, destination


sentence = "I am going to college."

subject, action, destination = understand_sentence(sentence)

print("Subject:", subject)
print("Action:", action)
print("Destination:", destination)