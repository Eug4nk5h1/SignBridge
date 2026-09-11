from src.nlp import analyze_sentence
from src.translator import translate_to_asl


sentences = [
    "I am going to college.",
    "Where are you going?",
    "What are you doing?",
    "She is reading a book.",
    "I will come tomorrow."
]


for sentence in sentences:

    analysis = analyze_sentence(sentence)

    signs = translate_to_asl(analysis)

    print("\nEnglish:", sentence)
    print("ASL:", " → ".join(signs))