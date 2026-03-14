# File: user_store.py | Phase: 4
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def _get_connection():
    """Helper to get a database connection that returns rows as dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    print("[DB] Initializing SQLite database...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number   TEXT UNIQUE NOT NULL,
                name           TEXT NOT NULL,
                wallet_address TEXT NOT NULL,
                created_at     TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if table is empty to seed initial data
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            print("[DB] Seeding initial user data...")
            seed_data = [
                ('+911111111111', 'Alice', '0xAAAAReplaceWithRealTestnetAddr'),
                ('+912222222222', 'Bob', '0xBBBBReplaceWithRealTestnetAddr'),
                ('+913333333333', 'Rahul', '0xCCCCReplaceWithRealTestnetAddr'),
                ('+914444444444', 'Sarah', '0xDDDDReplaceWithRealTestnetAddr')
            ]
            conn.executemany("INSERT INTO users (phone_number, name, wallet_address) VALUES (?, ?, ?)", seed_data)
            conn.commit()

# Run initialization on import
init_db()

def add_user(phone: str, name: str, wallet: str) -> bool:
    """Add a new user to the database."""
    try:
        with _get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO users (phone_number, name, wallet_address) VALUES (?, ?, ?)", 
                         (phone, name, wallet))
            return conn.total_changes > 0
    except Exception as e:
        print(f"[DB][ERROR] Failed to add user: {e}")
        return False

def get_wallet_by_name(name: str) -> str | None:
    """Look up a user's wallet address by their name (case-insensitive)."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT wallet_address FROM users WHERE LOWER(name) = LOWER(?)", (name,))
            row = cursor.fetchone()
            return row['wallet_address'] if row else None
    except Exception as e:
        print(f"[DB][ERROR] get_wallet_by_name failed: {e}")
        return None

def get_wallet_by_phone(phone: str) -> str | None:
    """Look up a user's wallet address by their phone number."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT wallet_address FROM users WHERE phone_number = ?", (phone,))
            row = cursor.fetchone()
            return row['wallet_address'] if row else None
    except Exception as e:
        print(f"[DB][ERROR] get_wallet_by_phone failed: {e}")
        return None

def get_name_by_phone(phone: str) -> str | None:
    """Look up a user's name by their phone number."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT name FROM users WHERE phone_number = ?", (phone,))
            row = cursor.fetchone()
            return row['name'] if row else None
    except Exception as e:
        print(f"[DB][ERROR] get_name_by_phone failed: {e}")
        return None

def is_registered(phone: str) -> bool:
    """Check if a phone number is registered in the database."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT 1 FROM users WHERE phone_number = ?", (phone,))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"[DB][ERROR] is_registered failed: {e}")
        return False

def get_all_users() -> list:
    """Return all registered users as a list of dictionaries."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"[DB][ERROR] get_all_users failed: {e}")
        return []

if __name__ == '__main__':
    print("\n--- Testing Database ---")
    users = get_all_users()
    for u in users:
        print(u)
    
    print("\nBob's wallet:", get_wallet_by_name('Bob'))
    print("Is +911111111111 registered?", is_registered('+911111111111'))
