from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.video import extract_audio
from app.transcription import transcribe_audio
from app.analyzer import analyze_transcript

from dotenv import load_dotenv


load_dotenv()


app = FastAPI(title="Video Autopsy")


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    try:

        # -------------------------
        # CHECK FILE
        # -------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No video file was selected."
            )


        if not file.content_type or not file.content_type.startswith("video/"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid video file."
            )


        # -------------------------
        # SAVE VIDEO
        # -------------------------

        video_path = UPLOAD_DIR / file.filename

        audio_path = (
            OUTPUT_DIR /
            f"{Path(file.filename).stem}.mp3"
        )


        with open(video_path, "wb") as buffer:

            buffer.write(
                await file.read()
            )


        # -------------------------
        # EXTRACT AUDIO
        # -------------------------

        try:

            extract_audio(
                video_path,
                audio_path
            )

        except Exception as e:

            print(
                f"\n❌ AUDIO EXTRACTION ERROR: {e}\n"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "We couldn't extract audio from this video. "
                    "Make sure the video file isn't corrupted."
                )
            )


        # -------------------------
        # TRANSCRIBE
        # -------------------------

        try:

            transcript = transcribe_audio(
                str(audio_path)
            )

        except Exception as e:

            print(
                f"\n❌ TRANSCRIPTION ERROR: {e}\n"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "We couldn't transcribe the audio. "
                    "Please try another video or check that "
                    "the video contains clear speech."
                )
            )


        # -------------------------
        # AI ANALYSIS
        # -------------------------

        try:

            analysis = analyze_transcript(
                transcript
            )

        except Exception as e:

            print(
                f"\n❌ AI ANALYSIS ERROR: {e}\n"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "The video was transcribed successfully, "
                    "but the AI analysis failed. "
                    "Please try again."
                )
            )


        # -------------------------
        # SUCCESS
        # -------------------------

        return {
            "filename": file.filename,
            "transcript": transcript,
            "analysis": analysis
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            f"\n❌ UNEXPECTED UPLOAD ERROR: {e}\n"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Something went wrong while processing "
                "your video. Please try again."
            )
        )