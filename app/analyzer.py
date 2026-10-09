import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import ANALYSIS_PROMPT


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def analyze_transcript(transcript: str):
    if not transcript.strip():
        return {
            "summary": "No speech detected.",
            "key_points": [],
            "sentiment": {
                "label": "Unknown",
                "explanation": "No speech was detected in the video."
            },
            "main_topics": [],
            "action_items": [],
        }

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    prompt = ANALYSIS_PROMPT.format(transcript=transcript)

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()
    print("\n===== AI RAW RESPONSE =====")
    print(content)
    print("===========================\n")
    
    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "summary": content,
            "key_points": [],
            "sentiment": {
                "label": "Unknown",
                "explanation": "The AI response could not be parsed."
            },
            "main_topics": [],
            "action_items": [],
        }


