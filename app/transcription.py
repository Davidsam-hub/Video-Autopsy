import os
import re

os.environ["PATH"] = (
    r"C:\Users\David Samuel\Downloads\ffmpeg-9.0.1-essentials_build\ffmpeg-9.0.1-essentials_build\bin"
    + os.pathsep
    + os.environ["PATH"]
)

import whisper

model = whisper.load_model("small")

def transcribe_audio(audio_path: str):
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False,
        temperature=0,
        condition_on_previous_text=True
    )

    text = result["text"].replace("<unk>", "").strip()

  
    replacements = {
        "turn on for this meeting": "turn up for this meeting",
        "turn off for this meeting": "turn up for this meeting",
        "miss you guys here": "meet you guys here",
        "turn off": "turn up",
    }

    for wrong, correct in replacements.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", correct, text, flags=re.IGNORECASE)

    return text