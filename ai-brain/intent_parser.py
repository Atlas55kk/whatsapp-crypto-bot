# File: intent_parser.py | Phase: 2
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from importlib import import_module
gemini_client = import_module("ai-brain.gemini_client")
call_gemini = gemini_client.call_gemini


def parse_intent(message_text):
    """Parse user message into structured intent dict via Gemini."""
    try:
        raw = call_gemini(message_text)
        # Strip any markdown code fences just in case
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        print(f"[AI] intent: {result}")
        return result
    except Exception as e:
        print(f"[AI][ERROR] Failed to parse intent: {e}")
        return {"action": "unknown"}


if __name__ == "__main__":
    tests = [
        "Send 5 HLUSD to Alice",
        "balance",
        "hello there"
    ]
    for msg in tests:
        print(f"\n--- Test: '{msg}' ---")
        result = parse_intent(msg)
        print(f"Result: {result}")
