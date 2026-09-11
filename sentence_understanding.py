try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except ImportError:
    nlp = None


def understand_sentence(sentence):
    if nlp is not None:
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
    else:
        words = [w.strip(".,!?") for w in sentence.split()]
        subject = words[0] if len(words) > 0 else None
        action = words[1] if len(words) > 1 else None
        destination = words[2] if len(words) > 2 else None
        return subject, action, destination


if __name__ == "__main__":
    sentence = "I am going to college."
    subject, action, destination = understand_sentence(sentence)
    print("Subject:", subject)
    print("Action:", action)
    print("Destination:", destination)