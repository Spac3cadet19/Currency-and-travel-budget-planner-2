"""

Currency and Travel Budget Planner - Streamlit UI.
Wires together CurrencyConverter, TripBudget, Expense, BudgetReport,
the holiday checker, and the AI advice helper.
"""

import streamlit as st
import requests
from datetime import date

from converter import CurrencyConverter
from trip_budget import TripBudget
from expense import Expense, parse_expense_text
from budget_report import BudgetReport
from holidays import get_holidays_in_range
from advice import get_travel_advice

COUNTRY_CODES = {
    "United States": "US",
    "United Kingdom": "GB",
    "France": "FR",
    "Germany": "DE",
    "Nigeria": "NG",
    "Canada": "CA",
    "Australia": "AU",
    "India": "IN",
    "South Africa": "ZA",
    "Ghana": "GH",
    "Kenya": "KE",
    "China": "CN",
    "Japan": "JP",
}

EXPENSE_CATEGORIES = ["Food", "Transport", "Accommodation", "Activities", "Shopping", "Other"]

st.set_page_config(page_title="Currency and Travel Budget Planner", layout="wide")
st.title("Currency and Travel Budget Planner")
st.write("Plan your trip budget, convert currencies, check holidays, and track expenses in one place.")

if "trip" not in st.session_state:
    st.session_state.trip = None

# --- SIDEBAR: API keys ---
st.sidebar.header("Settings")
exchange_api_key = st.sidebar.text_input(
    "Exchange Rate API key (optional)",
    type="password",
    help="Leave blank to use the built-in fallback exchange rates.",
)
gemini_api_key = st.sidebar.text_input("Gemini API key (optional, needed for travel advice)", type="password")

converter = CurrencyConverter(api_key=exchange_api_key if exchange_api_key else None)
if not exchange_api_key:
    st.sidebar.info("No exchange rate key entered, using built-in fallback rates.")

# --- SECTION 1: Trip Setup ---
st.header("1. Set Up Your Trip")

with st.form("trip_setup_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.selectbox("Destination country", list(COUNTRY_CODES.keys()))
        start_date = st.date_input("Start date", value=date.today())
        currency = st.text_input("Trip currency code (3 letters)", value="USD")
    with col2:
        end_date = st.date_input("End date", value=date.today())
        total_budget = st.number_input("Total budget", min_value=0.0, value=1000.0, step=50.0)

    setup_submitted = st.form_submit_button("Create Trip")

if setup_submitted:
    currency = currency.strip().upper()
    if not converter.is_valid_code(currency):
        st.error("Currency code must be exactly 3 uppercase letters, like USD or EUR.")
    elif end_date < start_date:
        st.error("End date cannot be before the start date.")
    else:
        st.session_state.trip = TripBudget(destination, start_date, end_date, total_budget, currency)
        st.success(f"Trip to {destination} created.")

trip = st.session_state.trip

if trip:
    report = BudgetReport(trip)

    st.subheader("Trip Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"{trip.total_budget:.2f} {trip.currency}")
    col2.metric("Trip Length", f"{trip.number_of_days()} days")
    col3.metric("Daily Limit", f"{trip.daily_limit():.2f} {trip.currency}")

    # --- SECTION 2: Currency Converter ---
    st.header("2. Currency Converter")
    c1, c2, c3 = st.columns(3)
    convert_amount = c1.number_input("Amount to convert", min_value=0.0, value=100.0)
    from_currency = c2.text_input("From currency", value=trip.currency, key="from_curr")
    to_currency = c3.text_input("To currency", value="USD", key="to_curr")

    if st.button("Convert"):
        try:
            result = converter.convert(convert_amount, from_currency, to_currency)
            st.success(f"{convert_amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
        except ValueError as error:
            st.error(str(error))

    # --- SECTION 3: Comparison Tool ---
    st.header("3. Compare Two Countries")
    st.write("See how far the same amount of money goes in two different currencies.")

    c1, c2, c3 = st.columns(3)
    base_amount = c1.number_input("Base amount", min_value=0.0, value=100.0, key="comp_amount")
    base_currency = c1.text_input("Base currency", value="USD", key="comp_base")
    compare_currency_1 = c2.text_input("Compare to currency 1", value="EUR", key="comp_1")
    compare_currency_2 = c3.text_input("Compare to currency 2", value="GBP", key="comp_2")

    if st.button("Compare"):
        try:
            results = report.compare_currencies(
                converter, base_amount, base_currency, compare_currency_1, compare_currency_2
            )
            side1, side2 = st.columns(2)
            side1.metric(compare_currency_1.upper(), f"{results[compare_currency_1.upper()]:.2f}")
            side2.metric(compare_currency_2.upper(), f"{results[compare_currency_2.upper()]:.2f}")
        except ValueError as error:
            st.error(str(error))

    # --- SECTION 4: Holiday Warnings ---
    st.header("4. Holiday Warnings")
    country_code = COUNTRY_CODES.get(trip.destination)

    if st.button("Check for Holidays During My Trip"):
        try:
            holidays = get_holidays_in_range(country_code, trip.start_date, trip.end_date)
            if holidays:
                st.warning(f"Your trip overlaps with {len(holidays)} public holiday(s):")
                for holiday in holidays:
                    st.write(f"- {holiday['name']} on {holiday['date']}")
            else:
                st.info("No public holidays found during your trip dates.")
        except Exception as error:
            st.error(f"Could not check holidays right now: {error}")

    # --- SECTION 5: Expense Logger ---
    st.header("5. Expense Logger")
    tab_quick, tab_manual = st.tabs(["Quick Add", "Manual Entry"])

    with tab_quick:
        quick_text = st.text_input("Type an expense, like '$50 taxi' or '20 euros for dinner'", key="quick_expense")
        if st.button("Add Quick Expense"):
            try:
                amount_value, description = parse_expense_text(quick_text)
                trip.add_expense(Expense(description, "Other", amount_value, date.today()))
                st.success(f"Added: {description} - {amount_value:.2f} {trip.currency}")
            except ValueError as error:
                st.error(f"Could not parse that expense: {error}")

    with tab_manual:
        with st.form("manual_expense_form"):
            exp_description = st.text_input("Description")
            exp_category = st.selectbox("Category", EXPENSE_CATEGORIES)
            exp_amount = st.number_input("Amount", min_value=0.0, value=0.0)
            exp_date = st.date_input("Date", value=date.today(), key="manual_date")
            manual_submitted = st.form_submit_button("Add Expense")

        if manual_submitted:
            if exp_amount <= 0:
                st.error("Amount must be greater than zero.")
            elif not exp_description.strip():
                st.error("Please enter a description.")
            else:
                trip.add_expense(Expense(exp_description, exp_category, exp_amount, exp_date))
                st.success("Expense added.")

    if trip.expenses:
        st.subheader("Expense Summary")
        st.dataframe([e.to_dict() for e in trip.expenses], use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Spent", f"{trip.total_spent():.2f} {trip.currency}")
        c2.metric("Remaining Budget", f"{trip.remaining_budget():.2f} {trip.currency}")
        c3.metric("Daily Limit Remaining", f"{trip.daily_limit_remaining():.2f} {trip.currency}")

        if trip.remaining_budget() < 0:
            st.error("You have gone over your total budget.")
    else:
        st.info("No expenses logged yet.")

    # --- SECTION 6: Download Report ---
    st.header("6. Download Your Trip Report")

    d1, d2 = st.columns(2)
    d1.download_button("Download as JSON", data=report.to_json(), file_name="trip_budget.json", mime="application/json")
    d2.download_button("Download as CSV", data=report.to_csv(), file_name="trip_budget.csv", mime="text/csv")

    # --- SECTION 7: Travel Advice ---
    st.header("7. Travel Advice")
    if not gemini_api_key:
        st.info("Enter a Gemini API key in the sidebar to get travel advice.")
    else:
        if st.button("Get Travel Advice"):
            try:
                with st.spinner("Getting advice..."):
                    advice = get_travel_advice(
                        trip.destination, trip.total_budget, trip.currency, trip.number_of_days(), gemini_api_key
                    )
                st.write(advice)
            except requests.exceptions.RequestException as error:
                st.error(f"Network problem while contacting Gemini: {error}")
            except (KeyError, IndexError):
                st.error("Got a response back from Gemini but could not read it. Try again.")

else:
    st.info("Fill out the trip setup form above to get started.")
