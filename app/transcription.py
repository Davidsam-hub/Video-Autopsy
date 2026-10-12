import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure FFmpeg so Whisper can find it on Windows
ffmpeg_path = os.getenv("FFMPEG_PATH", "ffmpeg")

if os.path.isfile(ffmpeg_path):
    ffmpeg_directory = str(Path(ffmpeg_path).parent)
    os.environ["PATH"] = (
        ffmpeg_directory + os.pathsep + os.environ.get("PATH", "")
    )

import whisper

model = whisper.load_model("small")


def transcribe_audio(audio_path: str):
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False,
        temperature=0,
        condition_on_previous_text=True,
    )

    text = result["text"].replace("<unk>", "").strip()

    replacements = {
        "turn on for this meeting": "turn up for this meeting",
        "turn off for this meeting": "turn up for this meeting",
        "miss you guys here": "meet you guys here",
        "turn off": "turn up",
    }

    for wrong, correct in replacements.items():
        text = re.sub(
            rf"\b{re.escape(wrong)}\b",
            correct,
            text,
            flags=re.IGNORECASE,
        )

    return text