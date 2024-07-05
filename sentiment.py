import streamlit as st
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def classify_sentiment(score):
    if score >= 0.6:
        return 5
    elif score >= 0.2:
        return 4
    elif score > -0.2:
        return 3
    elif score > -0.6:
        return 2
    else:
        return 1


def sentiment_analysis_page(chat_data):
    st.markdown('<h2 class="sub-title">Sentiment Analysis</h2>', unsafe_allow_html=True)

    analyzer = SentimentIntensityAnalyzer()
    chat_by_month = chat_data['chat_by_month']
    sentiment_results = {}
    message_counts = {month: len(messages) for month, messages in chat_by_month.items()}

    progress_bar = st.progress(0)
    total_months = len(chat_by_month)
    for i, (month, messages) in enumerate(chat_by_month.items()):
        combined_text = ' '.join(messages)
        sentiment_score = analyzer.polarity_scores(combined_text)["compound"]
        print(f"Month: {month}, Combined Text: {combined_text[:200]}...")  # Print first 200 chars for readability
        print(f"Month: {month}, Raw Sentiment Score: {sentiment_score}")  # Debug print for raw score
        sentiment_results[month] = classify_sentiment(sentiment_score)
        progress_bar.progress((i + 1) / total_months)

    # Display sentiment results
    st.markdown('<h3 class="sub-title">Monthly Sentiment Scores</h3>', unsafe_allow_html=True)
    months = list(sentiment_results.keys())
    sentiments = [sentiment_results[month] for month in months]
    counts = [message_counts[month] for month in months]

    fig, ax1 = plt.subplots()

    color = '#d6336c'
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sentiment Score", color=color)
    ax1.plot(months, sentiments, marker='o', color=color, label='Sentiment Score')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = '#ff4b4b'
    ax2.set_ylabel("Number of Messages", color=color)
    ax2.bar(months, counts, color=color, alpha=0.6, label='Number of Messages')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    fig.tight_layout()  # to ensure the right y-label is not slightly clipped
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    if st.button("Back"):
        st.session_state.page = 'upload'
        st.experimental_rerun()
