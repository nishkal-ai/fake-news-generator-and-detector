# --- Import Required Libraries ---
from dotenv import load_dotenv
import os
import openai
import streamlit as st

# --- Load API Key from .env file ---
load_dotenv()
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = os.getenv("GROQ_API_KEY")

# --- App Title & Description ---
st.title("📰 Fake News Generator & Detector")
st.subheader("Powered by Generative AI (Groq Llama 3)")

# --- User Inputs ---
topic = st.text_input("Enter a topic (e.g., politics, health, technology):")
tone = st.selectbox("Select a tone for generated news:", 
                    ["Clickbait", "Sarcastic", "Serious", "Satirical"])
mode = st.radio("What would you like to do?", 
                ["Generate Only", "Detect Only", "Generate + Detect"])

# --- Function to Generate Fake News ---
def generate_fake_news(topic: str, tone: str) -> str:
    """
    Generate a fake news headline and article based on user-selected topic and tone.
    """
    prompt = f"Create a fake news headline and short article about '{topic}' in a '{tone}' style."
    
    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=300
    )
    
    return response.choices[0].message["content"]

# --- Function to Detect Fake News ---
def detect_fake_news(article: str) -> str:
    """
    Analyze a news article and determine if it is fake, biased, or misleading.
    """
    prompt = f"Examine the following text and say if it seems fake, biased, or misleading:\n\n{article}"
    
    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=250
    )
    
    return response.choices[0].message["content"]

# --- Main Logic: Display Outputs Based on Mode ---
if topic and mode:
    with st.spinner("Processing... Please wait"):
        # --- Generate Fake News Only ---
        if mode == "Generate Only":
            article = generate_fake_news(topic, tone)
            st.write("### 📰 Generated Fake News")
            st.write(article)

        # --- Detect Fake News Only ---
        elif mode == "Detect Only":
            st.write("### 🕵️ Paste or Enter News Text to Detect")
            user_article = st.text_area("Paste the news article here:")
            
            if user_article:
                result = detect_fake_news(user_article)
                st.write("### 🔍 Detection Result")
                st.write(result)

        # --- Generate and Detect Together ---
        elif mode == "Generate + Detect":
            article = generate_fake_news(topic, tone)
            st.write("### 📰 Generated Fake News")
            st.write(article)

            result = detect_fake_news(article)
            st.write("### 🔍 Detection Result")
            st.write(result)

# --- Disclaimer ---
st.markdown("**Note: This is for educational and entertainment purposes only.**")
