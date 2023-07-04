import streamlit as st
from challenge_functions import sentiment_analysis as sa
import pandas as pd
import datetime


st.sidebar.markdown("# Sentiment Analysis")
st.sidebar.markdown(
    "Analyze the sentiment of the reviews, i.e., whether they are positive or negative."
)

st.markdown("# Sentiment Analysis")


uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = sa.load_csv_from_file_input(uploaded_file)

    with st.form("my_form"):
        st.markdown("### You can select the rows you want to analyze")

        st.dataframe(df)

        selected_list = st.multiselect("Index", df.index.to_list())
        print(selected_list)
        submitted = st.form_submit_button("Get predictions")

    if submitted:
        preds = sa.get_predictions(selected_list, df)
        if preds:
            preds_df = pd.DataFrame(preds, columns=["Text", "Label", "Score"])
            st.dataframe(preds_df)

            fname = f"Sentiment Analysis - {datetime.datetime.now().isoformat()}.csv"
            st.download_button(
                label="Download data as CSV",
                data=preds_df.to_csv(index=False).encode(),
                file_name=fname,
            )
        else:
            st.markdown(":red[No rows selected.]")
