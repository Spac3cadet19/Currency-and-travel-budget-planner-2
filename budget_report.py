import json
import csv
import io


class BudgetReport:

    def __init__(self, trip):
        self.trip = trip

    def compare_currencies(self, converter, amount, base_currency, currency_1, currency_2):

        result_1 = converter.convert(amount, base_currency, currency_1)
        result_2 = converter.convert(amount, base_currency, currency_2)
        return {
            currency_1.strip().upper(): result_1,
            currency_2.strip().upper(): result_2,
        }

    def to_json(self):
        data = {
            "destination": self.trip.destination,
            "start_date": str(self.trip.start_date),
            "end_date": str(self.trip.end_date),
            "currency": self.trip.currency,
            "total_budget": self.trip.total_budget,
            "total_spent": self.trip.total_spent(),
            "remaining_budget": self.trip.remaining_budget(),
            "expenses": [e.to_dict() for e in self.trip.expenses],
        }
        return json.dumps(data, indent=2)

    def to_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Description", "Category", "Amount", "Date"])
        for e in self.trip.expenses:
            writer.writerow([e.description, e.category, e.amount, e.date])
        return output.getvalue()
