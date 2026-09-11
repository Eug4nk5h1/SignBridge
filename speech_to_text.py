import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

# Make FFmpeg available to this Python program if path exists on local machine
ffmpeg_path = r"C:\Users\eugan\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.GPL_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-N-125875-g5d4d3bdc61-win64-gpl\bin"
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path


def record_and_transcribe(duration=5, sample_rate=16000, output_file="mic_test.wav"):
    print("Speak now...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )

    sd.wait()

    write(output_file, sample_rate, audio)

    print("Recording finished.")
    print("Loading Whisper...")

    model = whisper.load_model("base")

    result = model.transcribe(output_file)

    print("\nYou said:")
    print(result["text"])
    return result["text"]


if __name__ == "__main__":
    record_and_transcribe()