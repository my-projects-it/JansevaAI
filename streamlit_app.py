import streamlit as st
from firebase_config import save_user, validate_user, save_feedback
from chatbot import ask_ai
from alerts import get_govt_alerts
from utils import show_feedback_analytics

st.set_page_config(page_title="Citizen Help Platform", layout="wide", page_icon="🌐")

# ----- Sidebar: Login / Signup -----
st.sidebar.title("👤 Account")
choice = st.sidebar.selectbox("Choose Option", ["Login", "Signup"])

if choice == "Signup":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign Up"):
        save_user(email, password)
        st.sidebar.success("✅ Account Created! Please Login.")

elif choice == "Login":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if validate_user(email, password):
            st.session_state["user"] = email
            st.sidebar.success(f"Welcome, {email}!")
        else:
            st.sidebar.error("❌ Invalid Credentials!")

# ----- Main App -----
if "user" in st.session_state:
    st.markdown("<h1 style='text-align:center;color:#4B8BBE;'>🌐 Citizen Help Platform</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Tabbed Interface (Tirana-style)
    tabs = st.tabs(["📢 Alerts", "🤖 Ask AI", "📚 Resources", "✉️ Feedback", "📊 Analytics"])

    # --- Alerts Tab ---
    with tabs[0]:
        st.subheader("📢 Latest Alerts")
        alerts = get_govt_alerts()
        for alert in alerts:
            st.info(alert)

    # --- AI Chatbot Tab ---
    with tabs[1]:
        st.subheader("🤖 Ask AI")
        question = st.text_input("Type your question here and hit Ask:")
        if st.button("Ask AI"):
            if question:
                answer = ask_ai(question)
                st.success(answer)

    # --- Resources Tab ---
    with tabs[2]:
        st.subheader("📚 Resources & Help")
        st.markdown("- [Scholarships & Education](#)")
        st.markdown("- [Jobs & Skill Training](#)")
        st.markdown("- [Legal & Safety Guides](#)")
        st.markdown("- [Health & Awareness](#)")

    # --- Feedback Tab ---
    with tabs[3]:
        st.subheader("✉️ Feedback / Report Issue")
        feedback_msg = st.text_area("Type your message:")
        if st.button("Submit Feedback"):
            if feedback_msg:
                save_feedback(st.session_state["user"], feedback_msg)
                st.success("✅ Feedback Submitted!")

    # --- Analytics Tab (Admin Only) ---
    if st.session_state["user"] == "admin@domain.com":
        with tabs[4]:
            st.subheader("📊 Feedback Analytics")
            fig = show_feedback_analytics()
            if fig:
                st.plotly_chart(fig)
            else:
                st.info("No feedback yet.")
