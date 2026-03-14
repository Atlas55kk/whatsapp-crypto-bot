# File: app.py | Phase: 1
import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


def process_message(sender_phone, message_text):
    """Placeholder — will be wired in later phases."""
    pass


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """WhatsApp webhook verification (Twilio doesn't need this, kept for Meta compatibility)."""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        print("[WEBHOOK] Verification successful")
        return challenge, 200
    print("[WEBHOOK] Verification failed — bad token")
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    """Receive incoming WhatsApp messages via Twilio webhook."""
    try:
        # Twilio sends form data, not JSON
        sender_phone = request.form.get("From", "")
        message_text = request.form.get("Body", "")
        message_id = request.form.get("MessageSid", "")

        # Strip 'whatsapp:' prefix from sender number
        sender_phone = sender_phone.replace("whatsapp:", "")

        print(f"[WEBHOOK] from: {sender_phone} | msg: {message_text}")

        process_message(sender_phone, message_text)

    except Exception as e:
        print(f"[WEBHOOK][ERROR] {e}")

    # Always return 200 so Twilio doesn't retry
    return "OK", 200


if __name__ == "__main__":
    print("[WEBHOOK] Starting Flask server on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
