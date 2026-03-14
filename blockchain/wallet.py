# File: wallet.py | Phase: 3
import os
from dotenv import load_dotenv

load_dotenv()

BOT_WALLET_ADDRESS = os.getenv("BOT_WALLET_ADDRESS")
BOT_PRIVATE_KEY = os.getenv("BOT_PRIVATE_KEY")

def get_bot_address() -> str:
    """Get the bot's public wallet address from environment variables."""
    return BOT_WALLET_ADDRESS

def get_bot_key() -> str:
    """Get the bot's private key from environment variables."""
    return BOT_PRIVATE_KEY
