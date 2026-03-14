import sys
import os

# Ensure modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== SYSTEM DIAGNOSTIC TEST ===")

# 1. Test Database
try:
    from database.user_store import get_all_users, get_wallet_by_name
    users = get_all_users()
    print(f"✅ Database: OK ({len(users)} users found)")
    bob_wallet = get_wallet_by_name('Bob')
    if not bob_wallet:
        print("❌ Database: Failed to find Bob's wallet")
except Exception as e:
    print(f"❌ Database error: {e}")

# 2. Test Blockchain
try:
    from blockchain.hela_client import is_connected, get_balance
    from blockchain.wallet import get_bot_address
    connected = is_connected()
    if connected:
        bal = get_balance(get_bot_address())
        print(f"✅ Blockchain: OK (Connected to HeLa, Balance: {bal} HLUSD)")
    else:
        print("❌ Blockchain: Not connected to HeLa")
except Exception as e:
    print(f"❌ Blockchain error: {e}")

# 3. Test AI Brain
try:
    from importlib import import_module
    intent_parser = import_module("ai-brain.intent_parser")
    intent = intent_parser.parse_intent("What is my balance?")
    if intent.get('action') == 'balance':
        print(f"✅ AI Brain: OK (Parsed 'balance' correctly)")
    else:
        print(f"⚠️ AI Brain: Warning (Parsed as {intent.get('action')}) - Could be rate limited")
except Exception as e:
    print(f"❌ AI Brain error: {e}")

# 4. Test Webhook Modules
try:
    from ux_flow.message_templates import welcome_message
    from ux_flow.confirmation import store_pending, get_pending
    msg = welcome_message("Tester")
    store_pending("+123", {"test": "data"})
    p = get_pending("+123")
    if p and "Tester" in msg:
        print("✅ UX templates & memory: OK")
except Exception as e:
    print(f"❌ UX/Memory error: {e}")

print("==============================")
