import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, REVIEW_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def review_code(code: str) -> dict:
    prompt = REVIEW_PROMPT.format(code=code)

    response = model.generate_content(prompt)

    return {
        "review": response.text
    }