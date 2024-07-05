import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt


def parse_chat_history(lines):
    # Initialize a defaultdict to hold messages for each month
    chat_by_month = defaultdict(list)
    first_message = None
    last_message = None
    total_messages = 0
    total_word_count = 0
    message_dates = []

    # Initialize progress bar
    total_lines = len(lines)
    progress_bar = st.progress(0)

    for i, line in enumerate(lines):
        # Update progress bar
        progress_bar.progress((i + 1) / total_lines)

        # Example line format: "[1/1/22, 1:49:25 PM] Ece Ferah: Hey there!"
        if "]" in line and " - " not in line:
            try:
                timestamp_part, message_part = line.split("]", 1)
                timestamp_str = timestamp_part.strip("[")
                message = message_part.strip()

                # Ensure the timestamp is correctly parsed
                timestamp = datetime.strptime(timestamp_str, '%d/%m/%y, %I:%M:%S %p')
                month_str = timestamp.strftime('%Y-%m')

                chat_by_month[month_str].append(message)
                message_dates.append(timestamp.date())
                total_messages += 1
                total_word_count += len(message.split())

                # Capture the first and last messages
                if first_message is None:
                    first_message = (timestamp_str, message)
                last_message = (timestamp_str, message)
            except (ValueError, IndexError):
                # Handle lines that do not match the expected format
                continue

    # Calculate average number of messages per day
    if message_dates:
        num_days = (max(message_dates) - min(message_dates)).days + 1
        avg_messages_per_day = total_messages / num_days
    else:
        avg_messages_per_day = 0

    return chat_by_month, first_message, last_message, total_messages, total_word_count, avg_messages_per_day


def main():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #ff4b4b;
        }
        .sub-title {
            font-size: 24px;
            font-weight: bold;
            color: #d6336c;
        }
        .metric-box {
            border: 1px solid #d6336c;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;
        }
        .metric-value {
            font-size: 30px;
            font-weight: bold;
            color: #ff4b4b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="main-title">Relationship Analyzer</h1>', unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Upload your chat history", type="txt")

    if uploaded_file is not None:
        chat_history = uploaded_file.read().decode("utf-8").splitlines()
        st.text_area("Chat History Sample", "\n".join(chat_history[:100]), height=300)

        # Parse chat history
        with st.spinner('Parsing chat history...'):
            (chat_by_month, first_message, last_message, total_messages,
             total_word_count, avg_messages_per_day) = parse_chat_history(chat_history)

        # Display dashboard
        st.markdown('<h2 class="sub-title">Chat Analysis Dashboard</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("First Message")
            st.write(first_message[0])
            st.write(first_message[1])

        with col2:
            st.subheader("Last Message")
            st.write(last_message[0])
            st.write(last_message[1])

        st.markdown('<h3 class="sub-title">Key Metrics</h3>', unsafe_allow_html=True)
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.markdown(
                '<div class="metric-box"><div class="metric-value">{}</div><div>Total Number of Messages</div></div>'.format(
                    total_messages), unsafe_allow_html=True)
        with metrics_col2:
            st.markdown(
                '<div class="metric-box"><div class="metric-value">{}</div><div>Total Word Count</div></div>'.format(
                    total_word_count), unsafe_allow_html=True)
        with metrics_col3:
            st.markdown(
                '<div class="metric-box"><div class="metric-value">{}</div><div>Avg Messages per Day</div></div>'.format(
                    round(avg_messages_per_day)), unsafe_allow_html=True)

        # Prepare data for the bar chart
        months = list(chat_by_month.keys())
        message_counts = [len(messages) for messages in chat_by_month.values()]

        # Display bar chart
        st.markdown('<h3 class="sub-title">Messages by Month</h3>', unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.bar(months, message_counts, color='#d6336c')
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation=45)
        fig.tight_layout()
        st.pyplot(fig)


if __name__ == "__main__":
    main()
