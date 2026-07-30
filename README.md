# Currency and Travel Budget Planner

A Python + Streamlit app for planning a trip budget: convert currencies, calculate a daily spending limit, track expenses, compare travel costs between two countries, check for public holidays during your trip, and get AI-generated budget advice.

## Features

- **Currency conversion** — convert between currencies using live exchange rates, with a built-in fallback if no API key is provided
- **Trip budget math** — total budget, trip length, and daily spending limit, calculated automatically
- **Expense tracking** — log expenses by typing free text (e.g. "$50 taxi") or filling in a form; view a running summary of spend vs. remaining budget
- **Country comparison** — see how far the same amount of money goes in two different currencies
- **Holiday warnings** — checks whether your travel dates overlap with public holidays at your destination
- **AI travel advice** — sends your trip and budget details to the Gemini API for practical, personalized tips
- **Export** — download your trip budget and expense records as JSON or CSV

## Project structure

```
├── app.py              # Streamlit UI — wires all the classes together
├── converter.py         # CurrencyConverter — regex validation, exchange rate lookup
├── trip_budget.py        # TripBudget — daily limit, total budget tracking
├── expense.py            # Expense — add/edit/delete, save/load as CSV or JSON
├── budget_report.py      # BudgetReport — currency comparison, export to file
├── holidays.py           # Public holiday check via the Nager.Date API
├── advice.py             # AIAdvisor — travel budget advice via the Gemini API
└── requirements.txt      # Python dependencies
```

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/Spac3cadet19/Currency-and-travel-budget-planner-2.git
   cd Currency-and-travel-budget-planner-2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

   This opens the app in your browser at `http://localhost:8501`.

## API keys

The app works out of the box with built-in fallback exchange rates and no API keys. To enable live data, enter these in the app's sidebar:

- **Exchange Rate API key** — for live currency conversion rates
- **Gemini API key** — required for the AI travel advice feature


## Contributing

- Branch off `main` for your feature: `feature/your-feature-name`
- Open a pull request when ready — don't push directly to `main`
- Keep PRs scoped to one class/feature at a time