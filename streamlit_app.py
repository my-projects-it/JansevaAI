import streamlit as st
import pandas as pd
import os

# ==========================
# CSV Helper Functions
# ==========================

USERS_FILE = "users.csv"
FEEDBACK_FILE = "feedback.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["name", "email", "password"])

def save_user(name, email, password):
    df = load_users()
    # Check duplicate email
    if email in df["email"].values:
        return False
    new_user = pd.DataFrame([[name, email, password]], columns=df.columns)
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True

def validate_user(email, password):
    df = load_users()
    user = df[(df["email"] == email) & (df["password"] == password)]
    return not user.empty

def save_feedback(name, feedback):
    df = pd.DataFrame([[name, feedback]], columns=["name", "feedback"])
    if os.path.exists(FEEDBACK_FILE):
        old = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    return pd.DataFrame(columns=["name", "feedback"])


# ==========================
# Streamlit App
# ==========================

st.title("🛡️ JansevaAI - Secure Citizen App")

menu = ["Signup", "Login", "Feedback", "View Feedback"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Signup":
    st.subheader("Create a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if save_user(name, email, password):
            st.success("Signup successful! You can now login.")
        else:
            st.error("Email already exists. Please login.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_user(email, password):
            st.success(f"Welcome back, {email}!")
        else:
            st.error("Invalid email or password")

elif choice == "Feedback":
    st.subheader("Give Your Feedback")
    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback")
    if st.button("Submit Feedback"):
        save_feedback(name, feedback)
        st.success("Thank you for your feedback!")

elif choice == "View Feedback":
    st.subheader("📊 User Feedback")
    feedback_data = load_feedback()
    if not feedback_data.empty:
        st.dataframe(feedback_data)
    else:
        st.info("No feedback submitted yet.")
