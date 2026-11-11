import unittest
from finance_tracker.db import connect, add_transaction, list_transactions, summary

class FinanceTrackerTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_summarise(self):
        add_transaction(self.db, "income", "1000.00", "Work")
        add_transaction(self.db, "expense", "125.50", "Food")
        result = summary(self.db)
        self.assertEqual(result["income_cents"], 100000)
        self.assertEqual(result["expense_cents"], 12550)
        self.assertEqual(result["balance_cents"], 87450)

    def test_reject_invalid_amount_and_category(self):
        with self.assertRaises(ValueError):
            add_transaction(self.db, "expense", "-5", "Food")
        with self.assertRaises(ValueError):
            add_transaction(self.db, "expense", "5", "  ")

    def test_list_newest_first(self):
        add_transaction(self.db, "expense", "10", "Food")
        add_transaction(self.db, "expense", "20", "Travel")
        self.assertEqual(list_transactions(self.db)[0]["category"], "Travel")

if __name__ == "__main__":
    unittest.main()
