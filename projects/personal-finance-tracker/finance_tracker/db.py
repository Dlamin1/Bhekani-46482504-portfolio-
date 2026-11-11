"""SQLite persistence for the finance tracker."""
import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL CHECK (kind IN ('income', 'expense')),
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    category TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

def connect(database: str = "finance.db") -> sqlite3.Connection:
    """Open a database and ensure the schema exists."""
    path = Path(database)
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    return connection

def add_transaction(connection, kind: str, amount: str, category: str, note: str = "") -> int:
    if kind not in {"income", "expense"}:
        raise ValueError("kind must be 'income' or 'expense'")
    try:
        cents = round(float(amount) * 100)
    except (TypeError, ValueError) as exc:
        raise ValueError("amount must be a valid number") from exc
    if cents <= 0:
        raise ValueError("amount must be greater than zero")
    category = category.strip()
    if not category:
        raise ValueError("category cannot be empty")
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "INSERT INTO transactions(kind, amount_cents, category, note) VALUES (?, ?, ?, ?)",
            (kind, cents, category, note.strip()),
        )
        connection.commit()
        return int(cursor.lastrowid)

def list_transactions(connection, limit: int = 20):
    if limit < 1:
        raise ValueError("limit must be at least 1")
    return connection.execute(
        "SELECT id, kind, amount_cents, category, note, created_at "
        "FROM transactions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()

def summary(connection):
    rows = connection.execute(
        "SELECT kind, category, SUM(amount_cents) AS total_cents "
        "FROM transactions GROUP BY kind, category ORDER BY kind, category"
    ).fetchall()
    totals = {"income": 0, "expense": 0}
    categories = []
    for row in rows:
        totals[row["kind"]] += row["total_cents"]
        categories.append(dict(row))
    return {"income_cents": totals["income"], "expense_cents": totals["expense"],
            "balance_cents": totals["income"] - totals["expense"], "categories": categories}
