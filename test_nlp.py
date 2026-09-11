import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Test sentence
sentence = "I am going to college."

# Process the sentence
doc = nlp(sentence)

# Display the analysis
for token in doc:
    print(
        token.text,
        "→ POS:", token.pos_,
        "→ Dependency:", token.dep_
    )