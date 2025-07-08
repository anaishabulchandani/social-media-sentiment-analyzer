import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Social Media Sentiment Analyzer", layout="centered")

# --- BANNER IMAGE ---
if os.path.exists("banner.png"):
    st.image("banner.png", use_container_width=True)
else:
    st.warning("⚠️ banner.png not found.")
st.write("---")

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #6c63ff;'>📊 Social Media Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Upload your social media captions or type them manually and discover their emotional tone!</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("About")
st.sidebar.info("This app analyzes social media captions using TextBlob sentiment analysis. Built with 💜 by Anaisha Bulchandani.")

# --- INPUT CHOICE ---
st.header("📤 Upload CSV or Type Captions Manually")
input_method = st.radio("Choose input method:", ["Upload CSV", "Type manually"])

df = pd.DataFrame()

# --- OPTION 1: CSV Upload ---
if input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with a 'caption' column", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

# --- OPTION 2: Manual Input ---
elif input_method == "Type manually":
    manual_input = st.text_area("Type or paste your caption(s) below (one per line):", height=150)
    if manual_input.strip() != "":
        lines = [line.strip() for line in manual_input.split("\n") if line.strip()]
        df = pd.DataFrame(lines, columns=["caption"])

# --- SENTIMENT FUNCTION ---
def get_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.4:
        return "Positive 😊"
    elif polarity < -0.4:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# --- SENTIMENT ANALYSIS ---
if not df.empty:
    st.subheader("📄 Input Data")
    st.dataframe(df)

    df["Sentiment"] = df["caption"].apply(get_sentiment)

    st.subheader("🔍 Analysis Results")
    st.dataframe(df[["caption", "Sentiment"]])

    sentiment_counts = df["Sentiment"].value_counts()

    st.subheader("📊 Sentiment Distribution")
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Captions")
    st.pyplot(fig)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results CSV", csv, "analyzed_captions.csv", "text/csv")
