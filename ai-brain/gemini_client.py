# File: gemini_client.py | Phase: 2
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """You are a crypto transaction parser for a WhatsApp bot.
Extract the user's intent and return ONLY valid raw JSON.
No markdown, no code fences, no explanation. Only the JSON object.
Format:
{"action": "transfer"|"balance"|"unknown", "amount": number|null, "token": "HLUSD"|null, "recipient": string|null, "confidence": "high"|"low"}
Examples:
'Send 10 HLUSD to Bob' → {"action":"transfer","amount":10,"token":"HLUSD","recipient":"Bob","confidence":"high"}
'check my balance'     → {"action":"balance","amount":null,"token":null,"recipient":null,"confidence":"high"}
'hello'                → {"action":"unknown","amount":null,"token":null,"recipient":null,"confidence":"low"}
"""


def call_gemini(user_message):
    """Send user message to Gemini with system instruction and return raw response."""
    try:
        full_prompt = SYSTEM_PROMPT + "\nUser message: " + user_message
        response = model.generate_content(full_prompt)
        print(f"[GEMINI] Raw response: {response.text.strip()}")
        return response.text.strip()
    except Exception as e:
        print(f"[GEMINI][ERROR] {e}")
        return '{"action": "unknown"}'
