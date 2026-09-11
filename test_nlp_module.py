from src.nlp import analyze_sentence

sentences = [
    "I am going to college.",
    "Where are you going?",
    "What are you doing?",
    "She is reading a book.",
    "I will come tomorrow."
]

for sentence in sentences:

    print("=" * 40)
    print(sentence)

    analysis = analyze_sentence(sentence)

    for key, value in analysis.items():
        print(f"{key:15}: {value}")
        