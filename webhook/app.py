# File: app.py | Phase: 6
import os
import sys

# Load all modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request
from dotenv import load_dotenv

from webhook.handler import send_message
from importlib import import_module
intent_parser = import_module("ai-brain.intent_parser")
parse_intent = intent_parser.parse_intent

from blockchain.hela_client import get_balance
from blockchain.transaction import send_tokens
from database.user_store import (is_registered, get_wallet_by_name,
                                 get_wallet_by_phone, get_name_by_phone)
import ux_flow.message_templates as tmpl
from ux_flow.confirmation import store_pending, get_pending, clear_pending

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


def process_message(sender: str, text: str):
    """Main bot logic: routing, AI parsing, and blockchain execution."""
    try:
        # Prevent empty messages from crashing
        if not text:
            return

        text_upper = text.strip().upper()
        text_lower = text.strip().lower()

        # BLOCK 1 — YES/NO confirmation:
        if text_upper == 'YES':
            pending = get_pending(sender)
            if pending:
                send_message(sender, "⏳ Processing transaction on HeLa testnet...")
                tx = send_tokens(pending['to_address'], pending['amount'])
                
                if tx:
                    msg = tmpl.success_message(pending['amount'], pending['token'], pending['recipient'], tx)
                else:
                    msg = tmpl.error_message('blockchain_error')
                
                clear_pending(sender)
            else:
                msg = '❌ No pending transaction found. Please start a new one.'
            send_message(sender, msg)
            return

        if text_upper == 'NO':
            clear_pending(sender)
            send_message(sender, '❌ Cancelled. No tokens were sent.')
            return

        # BLOCK 2 — New user check:
        if not is_registered(sender):
            send_message(sender, tmpl.welcome_message("there stranger"))
            return

        # BLOCK 3 — Help/greeting shortcuts:
        if text_lower in ['help', 'hi', 'hello', 'start', 'hey']:
            send_message(sender, tmpl.help_message())
            return

        # BLOCK 4 — Parse with Gemini AI:
        intent = parse_intent(text)
        action = intent.get('action', 'unknown')

        if action == 'transfer':
            amount = intent.get('amount')
            recipient = intent.get('recipient')
            token = intent.get('token', 'HLUSD')
            
            if not amount or not recipient:
                send_message(sender, tmpl.error_message('invalid_command'))
                return
                
            to_addr = get_wallet_by_name(recipient)
            if not to_addr:
                send_message(sender, tmpl.error_message('recipient_not_found'))
                return
                
            # Store pending details for YES/NO step
            store_pending(sender, {
                'to_address': to_addr, 
                'amount': amount,
                'token': token, 
                'recipient': recipient
            })
            send_message(sender, tmpl.confirm_transfer_message(amount, token, recipient))

        elif action == 'balance':
            wallet = get_wallet_by_phone(sender)
            name = get_name_by_phone(sender) or 'User'
            bal = get_balance(wallet) if wallet else 0
            send_message(sender, tmpl.balance_message(name, bal))

        else:
            send_message(sender, tmpl.error_message('invalid_command'))

    except Exception as e:
        print(f"[PROCESS][ERROR] {e}")


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """WhatsApp webhook verification (Meta compatibility)."""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        print("[WEBHOOK] Verification successful")
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    """Receive incoming WhatsApp messages (Twilio formatted)."""
    try:
        sender_phone = request.form.get("From", "").replace("whatsapp:", "")
        message_text = request.form.get("Body", "")
        
        # Twilio sends empty webhook tests sometimes, ignore those
        if not sender_phone or not message_text:
            return "OK", 200

        print(f"[WEBHOOK] from: {sender_phone} | msg: {message_text}")
        process_message(sender_phone, message_text)

    except Exception as e:
        print(f"[WEBHOOK][ERROR] {e}")

    return "OK", 200


if __name__ == "__main__":
    print("[WEBHOOK] Starting Flask server on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
