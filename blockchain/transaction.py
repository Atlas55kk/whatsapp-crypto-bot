# File: transaction.py | Phase: 3
import sys
import os

# Add parent directory to path to allow importing adjacent modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from blockchain import hela_client, wallet

def send_tokens(to_address: str, amount_hlusd: float) -> str | None:
    """Send HLUSD tokens to a specified address on the HeLa testnet."""
    try:
        w3 = hela_client.w3
        bot_addr = wallet.get_bot_address()
        bot_key = wallet.get_bot_key()
        
        nonce = w3.eth.get_transaction_count(bot_addr)
        
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': w3.to_wei(amount_hlusd, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 666888
        }
        
        signed = w3.eth.account.sign_transaction(tx, bot_key)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        hash_str = tx_hash.hex()
        
        print(f"[TX] Sent {amount_hlusd} HLUSD → {to_address} | hash: {hash_str}")
        return hash_str

    except Exception as e:
        print(f"[TX][ERROR] Transaction failed: {e}")
        return None

if __name__ == '__main__':
    print(hela_client.is_connected())
    print(hela_client.get_balance(wallet.get_bot_address()))
