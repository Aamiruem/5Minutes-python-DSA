
import streamlit as st
from textblob import TextBlob
import re
import pandas as pd

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def analyze_sentiment(feedback):
    blob = TextBlob(feedback)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

st.title("Customer Feedback Analyzer")

st.header("Enter Customer Feedback Below")
feedback_input = st.text_area("Feedback", "Type your feedback here...")

if st.button("Analyze Feedback"):
    if feedback_input:
        sentiment = analyze_sentiment(feedback_input)
        st.write(f"Sentiment: {sentiment}")
    else:
        st.write("Please enter some feedback to analyze.")



#requirements : streamlit, textblob, pandas