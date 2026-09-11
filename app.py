from src.speech import record_audio, speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl


print("=" * 60)
print("                 SIGNBRIDGE AI")
print("          SPEECH → ASL TRANSLATION")
print("=" * 60)


# ----------------------------------------
# STEP 1 — Speech Input
# ----------------------------------------

print("\n[1] SPEECH INPUT")

audio_file = record_audio()


# ----------------------------------------
# STEP 2 — Speech Recognition
# ----------------------------------------

print("\n[2] SPEECH RECOGNITION")

text = speech_to_text(audio_file)

print("Recognized English:")
print("👉", text)


# ----------------------------------------
# STEP 3 — NLP Analysis
# ----------------------------------------

print("\n[3] NLP & SENTENCE UNDERSTANDING")

analysis = analyze_sentence(text)

for key, value in analysis.items():
    print(f"{key:15}: {value}")


# ----------------------------------------
# STEP 4 — ASL Translation
# ----------------------------------------

print("\n[4] ENGLISH → ASL TRANSLATION")

sign_sequence = translate_to_asl(analysis)

print("ASL Sign Sequence:")
print(" → ".join(sign_sequence))


# ----------------------------------------
# COMPLETE
# ----------------------------------------

print("\n" + "=" * 60)
print("             TRANSLATION COMPLETED")
print("=" * 60)