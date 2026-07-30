"""

Connects to the Nager.Date public holidays API and checks whether any
holidays fall within a trip's date range.
"""

from datetime import datetime
import requests


def get_holidays_in_range(country_code, start_date, end_date):
    """Returns a list of {'name', 'date'} dicts for public holidays in the date range."""
    years_to_check = set([start_date.year, end_date.year])
    matching_holidays = []

    for year in years_to_check:
        try:
            url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            holidays = response.json()
        except requests.exceptions.RequestException:
            continue  # skip this year if the API is unreachable

        for holiday in holidays:
            holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d").date()
            if start_date <= holiday_date <= end_date:
                matching_holidays.append({"name": holiday["name"], "date": holiday_date})

    return matching_holidays
