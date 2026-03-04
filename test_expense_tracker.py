import unittest
from expense_tracker import ExpenseTracker
import tkinter as tk
import tempfile
import csv
import os

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = ExpenseTracker(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_total_calculation(self):
        self.app.expenses = [(10.0, "Food"), (20.5, "Transport")]
        total = self.app.update_total()
        self.assertEqual(total, 30.5)

    def test_invalid_input(self):
        self.app.amount_entry.insert(0, "abc")
        self.app.category_entry.insert(0, "Food")
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)

    def test_csv_save_load(self):
        self.app.expenses = [(5.0, "Coffee"), (15.0, "Lunch")]

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        temp_file.close()

        with open(temp_file.name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Amount", "Category"])
            writer.writerows(self.app.expenses)

        self.app.expenses.clear()
        self.app.listbox.delete(0, tk.END)

        with open(temp_file.name, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.app.expenses.append((float(row["Amount"]), row["Category"]))

        self.assertEqual(len(self.app.expenses), 2)
        os.unlink(temp_file.name)


if __name__ == "__main__":
    unittest.main()