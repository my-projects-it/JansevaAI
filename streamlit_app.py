# app.py
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import requests
import uuid

# ------------------------------
# Hugging Face Free AI Model
# ------------------------------
HF_API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN", "")

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

def get_ai_solution(problem_text):
    if not HF_API_TOKEN:
        return "Demo AI Solution: Please add HF_API_TOKEN in Streamlit Secrets for full AI suggestions."
    payload = {"inputs": problem_text, "parameters": {"max_new_tokens": 100}}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return f"AI API Error: {response.status_code}"
    except Exception as e:
        return f"AI API Exception: {str(e)}"

# ------------------------------
# Session State / Data Storage
# ------------------------------
if "problems" not in st.session_state:
    st.session_state.problems = []  # List of dicts: id, text, location, category, submission_time, solutions

# ------------------------------
# App Title
# ------------------------------
st.set_page_config(page_title="Citizen Problem Solver", layout="wide")
st.title("🛠️ Citizen Problem & Solution Tracker")
st.markdown("Submit problems, suggest solutions, vote, and track status with AI assistance!")

# ------------------------------
# Sidebar Navigation
# ------------------------------
menu = st.sidebar.selectbox("Menu", ["Submit Problem", "View Problems", "Hackathon / Leaderboard"])

# ------------------------------
# Submit Problem
# ------------------------------
if menu == "Submit Problem":
    st.header("Submit a Problem")
    problem_text = st.text_area("Describe your problem", "")
    category = st.selectbox("Category", ["Health", "Infrastructure", "Education", "Environment", "Other"])
    location = st.text_input("Location / City", "")
    
    if st.button("Submit Problem"):
        if problem_text and location:
            problem_id = str(uuid.uuid4())
            st.session_state.problems.append({
                "id": problem_id,
                "text": problem_text,
                "category": category,
                "location": location,
                "submission_time": datetime.now(),
                "solutions": [],  # each solution: dict: author, text, ai_generated, votes
                "deadline": datetime.now() + timedelta(days=7)  # internal alert simulation
            })
            st.success("Problem submitted successfully!")

# ------------------------------
# View Problems
# ------------------------------
elif menu == "View Problems":
    st.header("All Problems & Solutions")
    if not st.session_state.problems:
        st.info("No problems submitted yet.")
    else:
        for p in st.session_state.problems[::-1]:
            st.subheader(f"{p['text']} ({p['category']}, {p['location']})")
            st.caption(f"Submitted on: {p['submission_time'].strftime('%Y-%m-%d %H:%M:%S')} | Deadline: {p['deadline'].strftime('%Y-%m-%d')}")
            
            # AI Suggestion Button
            if st.button(f"AI Suggest Solution for {p['id']}", key=f"ai_{p['id']}"):
                ai_sol = get_ai_solution(p['text'])
                p['solutions'].append({"author": "AI", "text": ai_sol, "ai_generated": True, "votes": 0})
                st.success("AI solution added!")

            # Add User Solution
            with st.expander("Add Solution"):
                user_sol = st.text_area(f"Your Solution for {p['id']}", key=f"user_{p['id']}")
                if st.button(f"Submit Solution {p['id']}", key=f"submit_{p['id']}"):
                    if user_sol:
                        p['solutions'].append({"author": "User", "text": user_sol, "ai_generated": False, "votes": 0})
                        st.success("Solution added!")

            # Show Solutions
            if p['solutions']:
                st.markdown("**Solutions:**")
                for idx, s in enumerate(p['solutions']):
                    st.write(f"- {s['text']} (by {s['author']}) | Votes: {s['votes']}")
                    if st.button(f"Vote {p['id']}_{idx}", key=f"vote_{p['id']}_{idx}"):
                        s['votes'] += 1
                        st.success("Voted successfully!")

# ------------------------------
# Hackathon / Leaderboard
# ------------------------------
elif menu == "Hackathon / Leaderboard":
    st.header("Hackathon & Leaderboard")
    # Collect all solutions across problems
    all_solutions = []
    for p in st.session_state.problems:
        for s in p['solutions']:
            all_solutions.append({
                "problem": p['text'],
                "solution": s['text'],
                "author": s['author'],
                "votes": s['votes']
            })
    if not all_solutions:
        st.info("No solutions yet!")
    else:
        df = pd.DataFrame(all_solutions)
        st.dataframe(df.sort_values(by="votes", ascending=False))
