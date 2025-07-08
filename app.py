import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

st.title("📊 Social Media Sentiment Analyzer")
st.markdown("Made using Python & Streamlit")

st.sidebar.header("About")
st.sidebar.info("This app analyzes social media captions using TextBlob sentiment analysis.")



# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with a 'caption' column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show the uploaded data
    st.subheader("📄 Uploaded Data")
    st.write(df)

    # Sentiment analysis function
    def get_sentiment(text):
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.4:
            return "Positive 😊"
        elif polarity < -0.4:
            return "Negative 😞"
        else:
            return "Neutral 😐"

    # Apply analysis
    df["Sentiment"] = df["caption"].apply(get_sentiment)

    st.subheader("🔍 Analysis Results")
    st.write(df)

    # Show sentiment counts
    sentiment_counts = df["Sentiment"].value_counts()

    st.subheader("📊 Sentiment Distribution")
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Captions")
    st.pyplot(fig)

    # Download analyzed file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results CSV", csv, "analyzed_captions.csv", "text/csv")
