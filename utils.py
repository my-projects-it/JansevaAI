import pandas as pd
import plotly.express as px
from firebase_config import feedback_sheet

def show_feedback_analytics():
    feedbacks = feedback_sheet.get_all_records()
    if not feedbacks:
        return None
    df = pd.DataFrame(feedbacks)
    fig = px.bar(df, x='user_email', y='message', title="Feedback Analytics")
    return fig
