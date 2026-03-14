# File: hela_client.py | Phase: 3
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

HELA_RPC = os.getenv("HELA_RPC")
w3 = Web3(Web3.HTTPProvider(HELA_RPC))

if w3.is_connected():
    print("[HELA] Connected")
else:
    print("[HELA] FAILED")

def is_connected() -> bool:
    """Return whether the web3 instance is connected to the HeLa network."""
    return w3.is_connected()

def get_balance(wallet_address: str) -> float:
    """Get the HLUSD balance of a given wallet address."""
    try:
        raw = w3.eth.get_balance(wallet_address)
        return round(float(w3.from_wei(raw, 'ether')), 4)
    except Exception as e:
        print(f"[HELA][ERROR] get_balance failed: {e}")
        return 0.0
