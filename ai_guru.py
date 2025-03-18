import openai
import streamlit as st
import os
import sqlite3
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize SQLite Database for Memory
def init_db():
    conn = sqlite3.connect("ai_guru_memory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY, user_input TEXT, ai_response TEXT)''')
    conn.commit()
    conn.close()

init_db()

def save_interaction(user_input, ai_response):
    conn = sqlite3.connect("ai_guru_memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_input, ai_response) VALUES (?, ?)", (user_input, ai_response))
    conn.commit()
    conn.close()

def get_recent_history(limit=5):
    conn = sqlite3.connect("ai_guru_memory.db")
    c = conn.cursor()
    c.execute("SELECT user_input, ai_response FROM chat_history ORDER BY id DESC LIMIT ?", (limit,))
    history = c.fetchall()
    conn.close()
    return history

def get_ai_guru_response(user_input):
    """Get response from AI Guru."""
    prompt = f"""
    You are AI Guru, a deeply insightful mentor trained in the philosophies of Naval Ravikant, Stoicism, Vedanta, and Zen Buddhism. 
    Your response should be structured, deep, and reflective.
    User's Question: "{user_input}"
    AI Guru's Response:
    """
    
    client = openai.Client(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a wise mentor who helps people reflect deeply on their lives."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🧘‍♂️ AI Guru: Your Digital Self-Reflection Mentor")
st.write("Ask me a question about life, purpose, or decision-making. I will respond with thought-provoking questions and insights.")

# User input
user_input = st.text_input("Your Question:")

if st.button("Ask AI Guru"): 
    if user_input:
        response = get_ai_guru_response(user_input)
        save_interaction(user_input, response)
        st.write("🧘 AI Guru's Response:")
        st.write(response)
    else:
        st.write("Please enter a question for AI Guru.")

# Display Recent Conversations
st.write("## Recent Conversations")
history = get_recent_history()
for user_q, ai_resp in history:
    st.markdown(f"**You:** {user_q}")
    st.markdown(f"**AI Guru:** {ai_resp}")
    st.write("---")
