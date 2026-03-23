import os
import json
from dotenv import load_dotenv
from google import genai
from prompts import SYSTEM_PROMPT, REVIEW_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def review_code(code: str) -> dict:
    prompt = REVIEW_PROMPT.format(code=code)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
        },
    )

    return json.loads(response.text)