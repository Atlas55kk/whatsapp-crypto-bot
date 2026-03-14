# File: message_templates.py | Phase: 5

def welcome_message(name: str = 'there') -> str:
    """Friendly intro explaining what the bot does and listing example commands."""
    return (
        f"🤖 Hi {name}! I'm your WhatsApp Crypto Bot.\n\n"
        "I can help you send tokens and check your balance on the HeLa Testnet.\n\n"
        "Try sending me:\n"
        "💸 'Send 10 HLUSD to Alice'\n"
        "💰 'Balance'\n"
        "❓ 'Help'"
    )

def confirm_transfer_message(amount: float, token: str, recipient: str, fee: float = 0.01) -> str:
    """Clear summary of a pending transfer awaiting user confirmation."""
    return (
        f"💸 Transfer Summary\n"
        f"Send: {amount} {token}\n"
        f"To: {recipient}\n"
        f"Fee: {fee} {token}\n\n"
        "Reply YES to confirm or NO to cancel."
    )

def success_message(amount: float, token: str, recipient: str, tx_hash: str) -> str:
    """Success message with transaction hash and block explorer link."""
    short_hash = f"{tx_hash[:10]}..."
    explorer_link = f"https://testnet-blockexplorer.helachain.com/tx/{tx_hash}"
    return (
        f"✅ Success!\n"
        f"Sent {amount} {token} to {recipient}.\n\n"
        f"Hash: {short_hash}\n"
        f"View on Explorer: {explorer_link}"
    )

def balance_message(name: str, amount: float, token: str = 'HLUSD') -> str:
    """Simple balance display."""
    return f"💰 {name}, your current balance is:\n{amount} {token}"

def error_message(reason: str) -> str:
    """Friendly non-technical explanations for common errors."""
    errors = {
        'insufficient_balance': "❌ You don't have enough HLUSD for this transfer and the network fee.",
        'recipient_not_found': "❌ I couldn't find that person in my registry. Make sure they are registered.",
        'invalid_command': "❌ I didn't quite catch that. Type 'help' to see what I can do.",
        'blockchain_error': "❌ The HeLa blockchain encountered an error processing your request. Please try again later."
    }
    return errors.get(reason, "❌ An unknown error occurred. Please try again.")

def help_message() -> str:
    """Full command list with examples."""
    return (
        "❓ *Help & Commands*\n\n"
        "Here's what I can do for you:\n"
        "• Send crypto: 'Send 5 HLUSD to Bob'\n"
        "• Check balance: 'What is my balance?'\n"
        "• Help: 'Help me'\n\n"
        "Make sure to specify the exact recipient name!"
    )
