"""Command-line interface."""
import argparse
from contextlib import closing
from .db import connect, add_transaction, list_transactions, summary

def money(cents):
    return f"R{cents / 100:,.2f}"

def main():
    parser = argparse.ArgumentParser(description="Track income and expenses in a local SQLite database.")
    parser.add_argument("--db", default="finance.db", help="database file (default: finance.db)")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="record a transaction")
    add.add_argument("--kind", choices=("income", "expense"), required=True)
    add.add_argument("--amount", required=True, help="positive amount, e.g. 125.50")
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")
    listing = commands.add_parser("list", help="show recent transactions")
    listing.add_argument("--limit", type=int, default=20)
    commands.add_parser("summary", help="show totals and category breakdown")
    args = parser.parse_args()
    try:
        with closing(connect(args.db)) as connection:
            if args.command == "add":
                identifier = add_transaction(connection, args.kind, args.amount, args.category, args.note)
                print(f"Saved transaction #{identifier}.")
            elif args.command == "list":
                rows = list_transactions(connection, args.limit)
                if not rows:
                    print("No transactions yet.")
                for row in rows:
                    print(f"#{row['id']} {row['created_at']} | {row['kind']:7} | "
                          f"{money(row['amount_cents']):>12} | {row['category']} | {row['note']}")
            else:
                result = summary(connection)
                print(f"Income:  {money(result['income_cents'])}")
                print(f"Expense: {money(result['expense_cents'])}")
                print(f"Balance: {money(result['balance_cents'])}")
                print("\nBy category:")
                for item in result["categories"]:
                    print(f"  {item['kind']:7} {item['category']}: {money(item['total_cents'])}")
    except ValueError as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
