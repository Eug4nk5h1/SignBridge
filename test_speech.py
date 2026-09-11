from src.speech import record_audio, speech_to_text


audio_file = record_audio()

text = speech_to_text(audio_file)

print("\nYou said:")
print(text)