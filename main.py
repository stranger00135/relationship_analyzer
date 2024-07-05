import streamlit as st
from parse import parse_chat_history
from dashboard import display_dashboard
from sentiment import sentiment_analysis_page
from utils.styles import apply_custom_styles


def main():
    apply_custom_styles()

    st.markdown('<h1 class="main-title">Relationship Analyzer</h1>', unsafe_allow_html=True)

    # Page navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'

    if st.session_state.page == 'upload':
        # File uploader
        uploaded_file = st.file_uploader("Upload your chat history", type="txt")

        if uploaded_file is not None:
            try:
                chat_history = uploaded_file.read().decode("utf-8").splitlines()
                st.text_area("Chat History Sample", "\n".join(chat_history[:100]), height=300)

                # Parse chat history
                with st.spinner('Parsing chat history...'):
                    chat_data = parse_chat_history(chat_history)

                # Store chat_data in session state
                st.session_state.chat_data = chat_data

                # Display the dashboard
                display_dashboard(chat_data)

                if st.button("Run Sentiment Analysis"):
                    st.session_state.page = 'sentiment'
                    st.experimental_rerun()

            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif st.session_state.page == 'sentiment':
        if 'chat_data' in st.session_state:
            sentiment_analysis_page(st.session_state.chat_data)


if __name__ == "__main__":
    main()
