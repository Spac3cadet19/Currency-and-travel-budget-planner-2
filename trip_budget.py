"""

Trip-level budget math: daily spending limit, total budget tracking, and
holding the list of expenses for a trip.
"""


class TripBudget:
    """Tracks the trip details, the expense list, and daily spending math."""

    def __init__(self, destination, start_date, end_date, total_budget, currency):
        if total_budget < 0:
            raise ValueError("Total budget cannot be negative.")
        if end_date < start_date:
            raise ValueError("End date cannot be before the start date.")

        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.total_budget = total_budget
        self.currency = currency
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def total_spent(self):
        return sum(e.amount for e in self.expenses)

    def remaining_budget(self):
        return self.total_budget - self.total_spent()

    def number_of_days(self):
        days = (self.end_date - self.start_date).days + 1
        return max(days, 1)

    def daily_limit(self):
        return self.total_budget / self.number_of_days()

    def daily_limit_remaining(self):
        return self.remaining_budget() / self.number_of_days()
