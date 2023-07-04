import streamlit as st
import pandas as pd

@st.cache_data
def load_csv_from_file_input(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
):
    return pd.read_csv(uploaded_file)