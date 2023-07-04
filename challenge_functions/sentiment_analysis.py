import streamlit as st
import pandas as pd
from transformers import pipeline
import asyncio


@st.cache_data
def load_csv_from_file_input(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
):
    return pd.read_csv(uploaded_file)


@st.cache_resource  # 👈 Add the caching decorator
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