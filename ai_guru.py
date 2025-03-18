import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Function to generate AI Guru responses
def get_ai_guru_response(user_input):
    prompt = f"""
    You are AI Guru, a deeply insightful mentor trained in the philosophies of Naval Ravikant, Stoicism, Vedanta, and Zen Buddhism. 

    **Your response should always be:**
    - **Structured** with clear insights, examples, and analogies.
    - **Long and deep** (at least 5-7 sentences minimum).
    - **Reflective** (ask a follow-up question at the end to make the user think deeper).

    User's Question: "{user_input}"
    AI Guru's Response:
    """

    client = openai.OpenAI(api_key=API_KEY)  

    response = client.chat.completions.create(
        model="gpt-4-turbo",  
        messages=[
            {"role": "system", "content": "You are a wise mentor who helps people reflect deeply on their lives."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,  # Increased response length
        temperature=0.7  # Increased creativity
    )

    return response.choices[0].message.content.strip()

# Streamlit UI Setup
st.title("🧘‍♂️ AI Guru: Your Digital Self-Reflection Mentor")
st.write("Ask me a question about life, purpose, or decision-making. I will respond with thought-provoking questions and insights.")

# User input
user_input = st.text_input("Your Question:")

if st.button("Ask AI Guru"): 
    if user_input:
        response = get_ai_guru_response(user_input)
        st.write("🧘 AI Guru's Response:")
        st.write(response)
    else:
        st.write("Please enter a question for AI Guru.")