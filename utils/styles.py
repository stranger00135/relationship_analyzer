import streamlit as st

def apply_custom_styles():
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
