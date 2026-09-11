import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# Make FFmpeg available to this Python program
os.environ["PATH"] += os.pathsep + r"C:\Users\eugan\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.GPL_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-N-125875-g5d4d3bdc61-win64-gpl\bin"

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

print("Recording finished.")
print("Loading Whisper...")

model = whisper.load_model("base")

result = model.transcribe("mic_test.wav")

print("\nYou said:")
print(result["text"])