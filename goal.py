import streamlit as st
import google.generativeai as genai
import requests

# Set your Gemini API key
genai.configure(api_key="AIzaSyA7Mdbr84c66nNUJ_pWV-YZ1b8rNyYa5Ys")

# Replace with your actual n8n webhook URL
N8N_WEBHOOK_URL = "https://kanika004.app.n8n.cloud/webhook-test/daily-motivation"

# Function to get motivational content
def get_motivation(goal):
    prompt = f"""
    You are a motivational AI coach.

    A user has entered the following personal goal:
    "{goal}"

    Your task is to:
    1. Give a short, specific daily progress tip tailored to this goal.
    2. Generate a motivational quote with 2-3 emojis to keep the user inspired.

    Respond in this format:
    🎯 Goal: {goal}
    💡 Tip: [your tip here]
    💬 Quote: [your quote here]
    """

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🎯 Daily Motivation Generator")
st.write("Enter your goal, and get a custom daily tip + motivational quote!")

user_goal = st.text_input("What's your goal?", placeholder="e.g. Lose 10kg, Become a teacher, Learn Python")

if st.button("Get Motivation"):
    if user_goal:
        with st.spinner("Generating your boost..."):
            motivation = get_motivation(user_goal)

            # Display the motivation
            st.success("Here is your daily boost!")
            st.write(motivation)

            # Send to n8n webhook
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json={"goal": user_goal, "motivation": motivation}
                )
                if response.status_code == 200:
                    st.info("✅ Sent to n8n successfully!")
                else:
                    st.warning(f"⚠️ Webhook error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to send to n8n: {e}")
    else:
        st.warning("Please enter your goal first.")
