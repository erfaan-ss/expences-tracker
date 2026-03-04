import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expenses = []

        # UI
        tk.Label(root, text="Amount").grid(row=0, column=0)
        tk.Label(root, text="Category").grid(row=1, column=0)

        self.amount_entry = tk.Entry(root)
        self.category_entry = tk.Entry(root)

        self.amount_entry.grid(row=0, column=1)
        self.category_entry.grid(row=1, column=1)

        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Save CSV", command=self.save_csv).grid(row=3, column=0)
        tk.Button(root, text="Load CSV", command=self.load_csv).grid(row=3, column=1)

        self.total_label = tk.Label(root, text="Total: 0.00")
        self.total_label.grid(row=4, column=0, columnspan=2)

        self.listbox = tk.Listbox(root, width=40)
        self.listbox.grid(row=5, column=0, columnspan=2)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        if not amount or not category:
            messagebox.showerror("Error", "All fields required")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be numeric")
            return

        self.expenses.append((amount, category))
        self.listbox.insert(tk.END, f"{category}: {amount:.2f}")
        self.update_total()

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def update_total(self):
        total = sum(amount for amount, _ in self.expenses)
        self.total_label.config(text=f"Total: {total:.2f}")
        return total

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path:
            return

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category"])
            writer.writerows(self.expenses)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        self.expenses.clear()
        self.listbox.delete(0, tk.END)

        with open(path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row["Amount"])
                category = row["Category"]
                self.expenses.append((amount, category))
                self.listbox.insert(tk.END, f"{category}: {amount:.2f}")

        self.update_total()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()