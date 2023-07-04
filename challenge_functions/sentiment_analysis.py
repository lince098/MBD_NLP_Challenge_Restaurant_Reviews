import streamlit as st
from transformers import pipeline


@st.cache_resource  
def load_sentiment_analysis_model():
    return pipeline("sentiment-analysis")


def get_predictions(selected_list, df):
    print("get_predictions:selected list", selected_list)
    if selected_list:
        selected_rows = df.iloc[selected_list, :]
        text_column = selected_rows["body"].to_list()
        model = load_sentiment_analysis_model()
        preds = [
            {"Text": text, "Label": pred["label"], "Score": pred["score"]}
            for pred, text in zip(model(text_column), text_column)
        ]
        return preds
    return None