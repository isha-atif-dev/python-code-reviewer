import os
import json
from dotenv import load_dotenv
import anthropic
from prompts import SYSTEM_PROMPT, REVIEW_PROMPT

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def review_code(code: str) -> dict:
    prompt = REVIEW_PROMPT.format(code=code)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = message.content[0].text

    if "```" in raw_text:
        parts = raw_text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            try:
                return json.loads(part)
            except json.JSONDecodeError:
                continue

    return json.loads(raw_text.strip())