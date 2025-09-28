import streamlit as st
import pandas as pd
import os
from datetime import datetime
from firebase_config import save_user, validate_user, save_feedback

st.set_page_config(page_title="JanSevaAI", page_icon="🤖", layout="wide")

DATA_FILE = "users.csv"
FEEDBACK_FILE = "feedback.csv"

# -------- Helper Functions --------
def load_users():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["username", "password"])

def save_users(df):
    df.to_csv(DATA_FILE, index=False)

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    return pd.DataFrame(columns=["username", "feedback", "timestamp"])

def save_feedback_local(username, feedback):
    df = load_feedback()
    new_row = {"username": username, "feedback": feedback, "timestamp": datetime.now()}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

# --------- Login / Signup ---------
st.title("🇮🇳 JanSevaAI – Citizen Help Platform")

menu = st.sidebar.radio("Navigation", ["Login", "Sign Up", "Dashboard"])

if menu == "Sign Up":
    st.subheader("Create Your Account")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Sign Up"):
        df = load_users()
        if username in df['username'].values:
            st.error("❌ Username already exists!")
        else:
            new_user = pd.DataFrame({"username": [username], "password": [password]})
            df = pd.concat([df, new_user], ignore_index=True)
            save_users(df)
            st.success("✅ Account created! Go to Login page.")

elif menu == "Login":
    st.subheader("Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        df = load_users()
        user = df[(df['username'] == username) & (df['password'] == password)]
        if not user.empty:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid credentials")

if menu == "Dashboard":
    if st.session_state.get("logged_in", False):
        st.success(f"Welcome, {st.session_state['username']}! 🎉")
        st.write("Use this space to report problems, give feedback, and help improve society.")

        feedback = st.text_area("Share your feedback or idea 💡")
        if st.button("Submit Feedback"):
            save_feedback_local(st.session_state['username'], feedback)
            st.success("✅ Your feedback has been saved!")
        
        st.subheader("Community Feedback")
        df = load_feedback()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No feedback yet.")
    else:
        st.warning("⚠ Please login to access Dashboard.")
