"""

The AIAdvisor class: sends trip and budget details to the Gemini API and
returns AI-generated travel budget advice.
"""

from google import genai


class AIAdvisor:
    MODEL = "gemini-3.6-flash"

    def __init__(self, api_key: str):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("A valid Gemini API key is required.")
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Gemini API: {e}")

    def build_prompt(self, trip_details: dict) -> str:
        name    = trip_details.get("trip_name",     "My Trip")
        home    = trip_details.get("home_currency", "NGN")
        dest    = trip_details.get("dest_currency", "USD")
        budget  = trip_details.get("total_budget",  0)
        days    = trip_details.get("duration_days", 0)
        daily   = trip_details.get("daily_limit",   0)
        spent   = trip_details.get("total_spent",   0)
        remain  = trip_details.get("remaining",     0)
        country = trip_details.get("country",       "the destination")
        return (
            f"I am planning a trip called '{name}' to {country}.\n"
            f"Here are my travel budget details:\n\n"
            f"  Home Currency    : {home}\n"
            f"  Destination      : {dest} ({country})\n"
            f"  Total Budget     : {home} {budget:,.2f}\n"
            f"  Duration         : {days} days\n"
            f"  Daily Limit      : {dest} {daily:,.2f}\n"
            f"  Total Spent      : {dest} {spent:,.2f}\n"
            f"  Remaining Budget : {dest} {remain:,.2f}\n\n"
            f"Based on these numbers, please give me:\n"
            f"1. Practical tips to stay within my daily limit\n"
            f"2. Common money traps to avoid in {country}\n"
            f"3. Smart ways to stretch my remaining budget\n"
            f"4. A brief warning if my budget looks too tight\n\n"
            f"Keep your response friendly, specific, and actionable. "
            f"Use bullet points where helpful."
        )

    def get_advice(self, trip_details: dict) -> str:
        if not isinstance(trip_details, dict) or not trip_details:
            raise ValueError("Trip details must be a non-empty dictionary.")
        required = ["trip_name", "home_currency", "dest_currency",
                    "total_budget", "duration_days", "daily_limit"]
        missing = [k for k in required if k not in trip_details]
        if missing:
            raise ValueError(f"Missing trip details: {', '.join(missing)}")
        try:
            prompt   = self.build_prompt(trip_details)
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt
            )
            if not response or not response.text:
                raise ValueError("Gemini returned an empty response. Please try again.")
            return response.text.strip()
        except ValueError:
            raise
        except Exception as e:
            raise ConnectionError(f"Gemini API call failed: {e}")