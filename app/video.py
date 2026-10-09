import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_path: Path) -> Path:
    """
    Extract audio from a video using FFmpeg.
    """
    command = [
        r"C:\Users\David Samuel\Downloads\ffmpeg-9.0.1-essentials_build\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "mp3",
        "-y",
        str(output_path),
    ]

    subprocess.run(command, check=True)

    return output_path