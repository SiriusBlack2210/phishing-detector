import streamlit as st
import requests
import csv
import os
import pandas as pd
from datetime import datetime

# ✅ Secure API key from Streamlit Secrets
API_KEY = st.secrets["AIzaSyAJdUDGE3NTeIaK5tR9y4rB0FZLrdJroUo"]
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent"

# 🔍 Detect phishing using Gemini
def detect_phishing(email_text):
    prompt = f"""
You are a cybersecurity analyst. Analyze the following email and tell if it is a phishing attempt.
Provide a risk score from 0 to 100 and a short reason.

Email:
{email_text}

Result:
"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={API_KEY}",
        headers=headers,
        json=payload
    )

    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e}\nFull response:\n{response.text}"

# 📝 Save analysis to CSV
def log_to_csv(email, result):
    with open("results.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email, result.strip()])

# 🌐 Streamlit App UI
st.set_page_config(page_title="Phishing Detector", layout="centered")
st.title("🔐 Gemini Phishing Email Detector")

# ✍️ Input: paste or upload
st.subheader("📤 Paste Email OR Upload File")
email_text = st.text_area("Paste email content below:", height=150)

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
if uploaded_file is not None:
    email_text = uploaded_file.read().decode("utf-8")

# 🚨 Analyze
if st.button("Analyze"):
    if email_text.strip() == "":
        st.warning("Please provide email content.")
    else:
        with st.spinner("Analyzing with Gemini..."):
            result = detect_phishing(email_text)
            st.success("Analysis Complete")
            st.markdown(result)
            log_to_csv(email_text, result)
            st.info("✅ Result saved to `results.csv`")

# 📊 Show detection history
if os.path.exists("results.csv"):
    st.subheader("📊 Detection History")
    df = pd.read_csv("results.csv", names=["Timestamp", "Email", "Analysis"])
    st.dataframe(df.tail(10), use_container_width=True)
