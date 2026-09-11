import whisper
import os

os.environ["PATH"] += os.pathsep + r"C:\Users\eugan\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.GPL_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-N-125875-g5d4d3bdc61-win64-gpl\bin"

model = whisper.load_model("base")

result = model.transcribe("test_audio.mp4")

print(result["text"])