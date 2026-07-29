"""

Currency conversion: validates currency codes with regex, fetches exchange
rates (with a local fallback so the app still works with no API key), and
converts an amount from one currency to another.
"""

import re
import requests

# Fallback rates so the app still works with no API key.
# Each value is "how many units of this currency equal 1 USD".
FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 157.0,
    "NGN": 1550.0,
    "CAD": 1.36,
    "AUD": 1.50,
    "INR": 83.0,
    "ZAR": 18.5,
    "GHS": 15.0,
    "KES": 129.0,
    "CNY": 7.2,
}


class CurrencyConverter:
    """Checks currency codes, looks up rates, and converts between currencies."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.code_pattern = re.compile(r"^[A-Z]{3}$")

    def is_valid_code(self, code):
        """Returns True if code is exactly 3 uppercase letters, e.g. NGN, USD, GBP."""
        if not code:
            return False
        return bool(self.code_pattern.match(code.strip().upper()))

    def get_rate(self, currency_code):
        currency_code = currency_code.strip().upper()

        if not self.is_valid_code(currency_code):
            raise ValueError("Currency code must be 3 uppercase letters, like USD.")

        if self.api_key:
            try:
                url = f"https://openexchangerates.org/api/latest.json?app_id={self.api_key}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                rates = response.json().get("rates", {})
                if currency_code in rates:
                    return rates[currency_code]
            except requests.exceptions.RequestException:
                pass  # fall back quietly if the API call fails

        if currency_code in FALLBACK_RATES:
            return FALLBACK_RATES[currency_code]

        raise ValueError(f"No rate available for {currency_code}, try a common currency like USD or EUR.")

    def convert(self, amount, from_code, to_code):
        from_rate = self.get_rate(from_code)
        to_rate = self.get_rate(to_code)
        amount_in_usd = amount / from_rate
        return amount_in_usd * to_rate
