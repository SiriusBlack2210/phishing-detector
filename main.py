import requests
import csv
from datetime import datetime

# Gemini API setup
API_KEY = "AIzaSyAJdUDGE3NTeIaK5tR9y4rB0FZLrdJroUo"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent"

def detect_phishing(email_text):
    prompt = f"""
You are a cybersecurity analyst. Analyze the following email and tell if it is a phishing attempt.
Provide a risk score from 0 to 100 and a short reason.

Email:
{email_text}

Result:
"""

    headers = { "Content-Type": "application/json" }
    payload = {
        "contents": [ { "parts": [ { "text": prompt } ] } ]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={API_KEY}",
        headers=headers,
        json=payload
    )

    try:
        result = response.json()['candidates'][0]['content']['parts'][0]['text']
        return result
    except Exception as e:
        return f"Error: {e}\nFull response:\n{response.text}"

def log_to_csv(email, analysis):
    with open("results.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, email, analysis.strip()])

# === CLI Interaction ===
email = input("Paste the suspicious email text:\n")
analysis = detect_phishing(email)
print("\n" + analysis)

# Save result
log_to_csv(email, analysis)
print("\n✅ Logged to results.csv")
