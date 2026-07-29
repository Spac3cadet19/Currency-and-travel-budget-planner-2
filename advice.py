"""

Sends trip and budget details to the Gemini API and returns AI-generated
travel budget advice.
"""

import requests


def get_travel_advice(destination, total_budget, currency, num_days, gemini_key):
    """Sends a prompt to the Gemini API and returns the advice text."""
    prompt = (
        f"Give short, practical travel budgeting advice for a trip to {destination}. "
        f"The traveler has a total budget of {total_budget} {currency} for {num_days} days. "
        f"Keep it to about 4 short bullet points, no long paragraphs."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()
    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]
