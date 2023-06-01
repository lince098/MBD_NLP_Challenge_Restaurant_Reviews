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


async def sentiment_analisys_on_selected_rows(selected_rows: list):
    async_calls = [classify_sentiment(row["body"]) for row in selected_rows]
    predictions = await asyncio.gather(*async_calls)
    return predictions


async def classify_sentiment(text):
    model = load_sentiment_analysis_model()
    pred = model(text)
    pred = {"label": pred[0]["label"], "score": pred[0]["score"]}
    return pred
