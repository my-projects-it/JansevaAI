import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json

# Google Sheets credentials from Streamlit Secrets
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_json = json.loads(st.secrets["gsheet_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

user_sheet = client.open("CitizenHelpUsers").sheet1
feedback_sheet = client.open("CitizenHelpFeedback").sheet1

def save_user(email, password):
    user_sheet.append_row([email, password])

def validate_user(email, password):
    users = user_sheet.get_all_records()
    for u in users:
        if u["email"] == email and u["password"] == password:
            return True
    return False

def save_feedback(user_email)
