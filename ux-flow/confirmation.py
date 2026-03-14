# File: confirmation.py | Phase: 5

PENDING = {}

def store_pending(phone: str, data: dict) -> None:
    """Store transaction data awaiting user confirmation."""
    PENDING[phone] = data
    print(f"[PENDING] stored for {phone}")

def get_pending(phone: str) -> dict | None:
    """Retrieve pending transaction data for a user if it exists."""
    return PENDING.get(phone, None)

def clear_pending(phone: str) -> None:
    """Remove pending transaction data for a user."""
    if phone in PENDING:
        del PENDING[phone]
        print(f"[PENDING] cleared for {phone}")
