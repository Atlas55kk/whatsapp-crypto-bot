# File: handler.py | Phase: 1
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_message(to_number, text):
    """Send a WhatsApp message via Twilio."""
    try:
        # Ensure 'whatsapp:' prefix on recipient number
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"

        message = client.messages.create(
            body=text,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to_number
        )
        print(f"[SENT] to: {to_number} | sid: {message.sid}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send to {to_number}: {e}")
        return False
