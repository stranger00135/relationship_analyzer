import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter, defaultdict


def display_dashboard(chat_data):
    chat_by_month = chat_data['chat_by_month']
    first_message = chat_data['first_message']
    last_message = chat_data['last_message']
    total_messages = chat_data['total_messages']
    total_word_count = chat_data['total_word_count']
    avg_messages_per_day = chat_data['avg_messages_per_day']

    st.markdown('<h2 class="sub-title">Chat Analysis Dashboard</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("First Message")
        st.write(f"{first_message[0]}: {first_message[1]}")

    with col2:
        st.subheader("Last Message")
        st.write(f"{last_message[0]}: {last_message[1]}")

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
            '<div class="metric-box"><div class="metric-value">{:.2f}</div><div>Avg Messages per Day</div></div>'.format(
                avg_messages_per_day), unsafe_allow_html=True)

    months = list(chat_by_month.keys())
    message_counts = {month: len(messages) for month, messages in chat_by_month.items()}
    participants_messages = defaultdict(lambda: [0] * len(months))

    for month_index, month in enumerate(months):
        for message in chat_by_month[month]:
            sender = message.split(':')[0].strip()  # Assuming format is "Sender: message"
            participants_messages[sender][month_index] += 1

    participants = list(participants_messages.keys())
    participant_colors = ['#ff4b4b', '#d6336c'][:len(participants)]  # Using pink theme colors

    st.markdown('<h3 class="sub-title">Messages by Month</h3>', unsafe_allow_html=True)
    fig, ax = plt.subplots()

    bottom = [0] * len(months)
    for participant, color in zip(participants, participant_colors):
        counts = participants_messages[participant]
        ax.bar(months, counts, label=participant, bottom=bottom, color=color)
        for i in range(len(months)):
            bottom[i] += counts[i]

    for i, month in enumerate(months):
        total = message_counts[month]
        y_offset = 0
        for participant, color in zip(participants, participant_colors):
            count = participants_messages[participant][i]
            percentage = round((count / total) * 100) if total > 0 else 0
            ax.text(i, y_offset + count / 2, f'{percentage}', ha='center', va='center', fontsize=6, color='white')
            y_offset += count

    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Messages")
    plt.xticks(rotation=45, ha='right')
    ax.legend(title='Share of Voice (%)')
    fig.tight_layout()
    st.pyplot(fig)
