import pandas as pd
from textblob import TextBlob

df = pd.read_csv("captions.csv")

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.4:
        return "Positive 😊"
    elif polarity < -0.4:
        return "Negative 😞"
    else:
        return "Neutral 😐"

df["Sentiment"] = df["caption"].apply(get_sentiment)

print(df)

df.to_csv("captions_with_sentiment.csv", index=False)

import matplotlib.pyplot as plt

# Count number of each sentiment
sentiment_counts = df["Sentiment"].value_counts()

# Plot bar chart
plt.figure(figsize=(6, 4))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'])

# Add labels and title
plt.title("Sentiment Analysis of Social Media Captions")
plt.xlabel("Sentiment")
plt.ylabel("Number of Captions")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show chart
plt.tight_layout()
plt.show()

# Ask user if they want to see the chart
show_plot = input("\nDo you want to see the sentiment chart? (yes/no): ").strip().lower()

if show_plot == "yes":
    import matplotlib.pyplot as plt

    # Count number of each sentiment
    sentiment_counts = df["Sentiment"].value_counts()

    # Plot bar chart
    plt.figure(figsize=(6, 4))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'])
    plt.title("Sentiment Analysis of Social Media Captions")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Captions")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

