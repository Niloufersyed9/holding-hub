import sqlite3

DB_NAME = "holdings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            email TEXT,
            symbol TEXT,
            shares INTEGER,
            buy_price REAL,
            threshold REAL
        )
    """)
    conn.commit()
    conn.close()

def add_holding(email, symbol, shares, buy_price, threshold):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO holdings VALUES (?, ?, ?, ?, ?)",
        (email, symbol, shares, buy_price, threshold)
    )
    conn.commit()
    conn.close()

def get_holdings(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT symbol, shares, buy_price, threshold FROM holdings WHERE email=?",
        (email,)
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "symbol": r[0],
            "shares": r[1],
            "buy_price": r[2],
            "threshold": r[3]
        }
        for r in rows
    ]
