import streamlit as st
import openai

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set OpenAI API key
openai.api_key = openai_api_key

# Streamlit application
st.title("LLM Relationship Analyzer")

prompt = st.text_area("Enter the text to analyze")

if st.button("Analyze"):
    if prompt:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        st.write(response.choices[0].text)
    else:
        st.write("Please enter a prompt to analyze.")
