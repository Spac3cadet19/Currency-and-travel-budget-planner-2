"""

The Expense class, quick-text parsing for adding expenses (uses regex to
pull the amount out of free text), and save/load helpers so expense
records can be stored as CSV or JSON.
"""

import re
import csv
import json


class Expense:
    """Holds the details of a single expense."""

    def __init__(self, description, category, amount, expense_date):
        self.description = description
        self.category = category
        self.amount = amount
        self.date = expense_date

    def to_dict(self):
        return {
            "description": self.description,
            "category": self.category,
            "amount": self.amount,
            "date": str(self.date),
        }


def parse_expense_text(text):
    """
    Takes free text like "$50 taxi" or "20 euros for dinner" and returns
    (amount, description). Raises ValueError if no number is found.
    """
    match = re.search(r"(\d+\.?\d*)", text)
    if not match:
        raise ValueError("Could not find a number in that text.")

    amount = float(match.group(1))

    description = text.replace(match.group(1), "")
    description = re.sub(r"[\$\u20ac\u00a3]", "", description)
    description = re.sub(r"\b(usd|eur|gbp|dollars|euros|pounds|naira|ngn)\b", "", description, flags=re.IGNORECASE)
    description = description.strip(" ,.-")
    if not description:
        description = "Expense"

    return amount, description


def delete_expense(expenses, index):
    """Removes the expense at position `index` from the list, in place."""
    if index < 0 or index >= len(expenses):
        raise IndexError("No expense at that position.")
    expenses.pop(index)


def edit_expense(expenses, index, description=None, category=None, amount=None, expense_date=None):
    """Updates the given fields of the expense at position `index`, in place."""
    if index < 0 or index >= len(expenses):
        raise IndexError("No expense at that position.")
    expense = expenses[index]
    if description is not None:
        expense.description = description
    if category is not None:
        expense.category = category
    if amount is not None:
        expense.amount = amount
    if expense_date is not None:
        expense.date = expense_date


def save_expenses_json(expenses, filepath):
    """Writes a list of Expense objects to a JSON file."""
    with open(filepath, "w") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2)


def save_expenses_csv(expenses, filepath):
    """Writes a list of Expense objects to a CSV file."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Category", "Amount", "Date"])
        for e in expenses:
            writer.writerow([e.description, e.category, e.amount, e.date])


def load_expenses_json(filepath):
    """Reads a JSON file and returns a list of Expense objects."""
    with open(filepath, "r") as f:
        records = json.load(f)
    return [Expense(r["description"], r["category"], r["amount"], r["date"]) for r in records]


def load_expenses_csv(filepath):
    """Reads a CSV file and returns a list of Expense objects."""
    expenses = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(Expense(row["Description"], row["Category"], float(row["Amount"]), row["Date"]))
    return expenses
