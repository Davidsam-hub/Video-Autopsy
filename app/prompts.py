ANALYSIS_PROMPT = """
Analyze the following video transcript.

Return ONLY valid JSON. Do not include markdown, code fences, or any text outside the JSON.

Use exactly this structure:

{{
  "summary": "A concise 2-4 sentence summary of what the video is about.",
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "sentiment": {{
    "label": "Positive",
    "explanation": "Brief explanation of why this sentiment was chosen."
  }},
  "main_topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ],
  "action_items": [
    "Action item 1",
    "Action item 2"
  ]
}}

Rules:
- Sentiment label must be exactly one of: Positive, Negative, Neutral, Mixed, Unknown.
- Extract action items ONLY when they are explicitly stated or clearly supported by the transcript.
- Do NOT infer technical problems, audio/video settings, equipment issues, or other details unless they are explicitly mentioned in the transcript.
- Base the summary, key points, sentiment, topics, and action items strictly on the transcript.
- Focus on the main purpose and message of the speaker rather than isolated or unclear words.
- If the transcript contains no actionable tasks or next steps, return an empty array.
- Do not invent information that is not supported by the transcript.
- Keep the analysis concise and useful.
- Preserve the meaning and context of the speaker's words.
- Never reinterpret unclear words into a different scenario.
- If the transcript contains words that appear to be transcription errors, use the surrounding context to understand the speaker's intended meaning.
- The summary must describe the dominant message of the transcript.

Transcript:
{transcript}
"""

