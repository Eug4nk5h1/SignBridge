import sounddevice as sd
from scipy.io.wavfile import write

duration = 5
sample_rate = 16000

print("Speak now...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1
)

sd.wait()

write("mic_test.wav", sample_rate, audio)

print("Recording saved as mic_test.wav")