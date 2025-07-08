import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Sentiment & Mood Analyzer", layout="centered")

# --- BANNER IMAGE ---
if os.path.exists("banner.png"):
    st.image("banner.png", use_container_width=True)
else:
    st.warning("⚠️ banner.png not found.")
st.write("---")

# --- SIDEBAR MODE SELECT ---
st.sidebar.header("App Mode")
mode = st.sidebar.radio("What would you like to do?", ["Social Media Caption Analysis", "Mood Detector"])

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("This app analyzes sentiment in text using TextBlob — created by Anaisha Bulchandani.")

# --- COMMON SENTIMENT FUNCTION ---
def get_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.4:
        return "Positive 😊"
    elif polarity < -0.4:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# =======================
# MODE 1: SOCIAL ANALYSIS
# =======================
if mode == "Social Media Caption Analysis":
    st.markdown("<h1 style='text-align: center; color: #6c63ff;'>📊 Social Media Sentiment Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Upload your social media captions or type them manually to discover their emotional tone!</p>", unsafe_allow_html=True)

    st.header("📤 Upload CSV or Type Captions Manually")
    input_method = st.radio("Choose input method:", ["Upload CSV", "Type manually"])

    df = pd.DataFrame()

    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload a CSV file with a 'caption' column", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

    elif input_method == "Type manually":
        manual_input = st.text_area("Type or paste your caption(s) below (one per line):", height=150)
        if st.button("🔍 Analyze") and manual_input.strip() != "":
            lines = [line.strip() for line in manual_input.split("\n") if line.strip()]
            df = pd.DataFrame(lines, columns=["caption"])

    if not df.empty:
        st.subheader("📝 Captions Provided by You")
        for cap in df["caption"]:
            st.markdown(f"- {cap}")

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


# =======================
# MODE 2: MOOD DETECTOR
# =======================
elif mode == "Mood Detector":
    st.markdown("<h1 style='text-align: center; color: #6c63ff;'>Mood Detector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Answer a few questions, and let us sense your mood through sentiment analysis.</p>", unsafe_allow_html=True)

    q1 = st.text_input("1. How are you feeling today?")
    q2 = st.text_input("2. What made you happy or upset recently?")
    q3 = st.text_input("3. What’s on your mind right now?")

    if st.button("🔍 Analyze My Mood"):
        responses = [q1, q2, q3]
        sentiments = [TextBlob(r).sentiment.polarity for r in responses if r.strip()]

        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)

            if avg_sentiment > 0.3:
                mood = "Positive 😊"
            elif avg_sentiment < -0.3:
                mood = "Negative 😞"
            else:
                mood = "Neutral 😐"

            st.success(f"Your overall mood seems to be: **{mood}**")

            st.markdown("### Sentiment per Answer:")
            for i, s in enumerate(sentiments):
                label = "Positive" if s > 0 else "Negative" if s < 0 else "Neutral"
                st.write(f"Q{i+1}: {label} ({s:.2f})")
        else:
            st.warning("Please answer at least one question.")
