from src.speech import record_audio, speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl
from src.sign_generator import play_sign_sequence


print("=" * 60)
print("                 SIGNBRIDGE AI")
print("          SPEECH → ASL TRANSLATION")
print("=" * 60)


# -------------------------------------------------
# 1. SPEECH INPUT
# -------------------------------------------------

print("\n[1] SPEECH INPUT")
audio_file = record_audio()


# -------------------------------------------------
# 2. SPEECH RECOGNITION
# -------------------------------------------------

print("\n[2] SPEECH RECOGNITION")

text = speech_to_text(audio_file)

print("Recognized English:")
print("👉", text)


# -------------------------------------------------
# 3. NLP & SENTENCE UNDERSTANDING
# -------------------------------------------------

print("\n[3] NLP & SENTENCE UNDERSTANDING")

analysis = analyze_sentence(text)

for key, value in analysis.items():
    print(f"{key:15}: {value}")


# -------------------------------------------------
# 4. ENGLISH → ASL TRANSLATION
# -------------------------------------------------

print("\n[4] ENGLISH → ASL TRANSLATION")

sign_sequence = translate_to_asl(analysis)

print("ASL Sign Sequence:")
print(" → ".join(sign_sequence))


# -------------------------------------------------
# 5. SIGN RETRIEVAL & VISUAL OUTPUT
# -------------------------------------------------

print("\n[5] SIGN RETRIEVAL & VISUAL OUTPUT")

print("Searching for ASL sign videos...")

for sign in sign_sequence:
    print(f"Finding {sign}...")

print("\n▶ Starting ASL video playback...")
print("Press Q to stop playback.")

play_sign_sequence(
    sign_sequence,
    display_window=True
)


# -------------------------------------------------
# COMPLETE
# -------------------------------------------------

print("\n" + "=" * 60)
print("             TRANSLATION COMPLETED")
print("=" * 60)