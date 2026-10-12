import os
import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_path: Path) -> Path:
    """Extract audio from a video using FFmpeg."""

    ffmpeg_path = os.environ.get("FFMPEG_PATH", "ffmpeg")

    subprocess.run(
        [
            ffmpeg_path,
            "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "libmp3lame",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return output_path

