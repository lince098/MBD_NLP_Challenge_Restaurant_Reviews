import streamlit as st
from challenge_functions import answer_reviews as ar, general as g
import pandas as pd
import datetime

st.sidebar.markdown("# Automated Responses")

st.markdown("# Automated Responses")
st.sidebar.markdown(
    "Automate responses for your reviews. Given a dataset, this feature will let you download a csv with the best answer for each review."
)

uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = g.load_csv_from_file_input(uploaded_file)
    with st.form("my_form"):
        st.markdown("### You can select the rows you want to analyze")

        st.dataframe(df)

        selected_list = st.multiselect("Index", df.index.to_list())
        submitted = st.form_submit_button("Get Answers")

    if submitted:
        preds = ar.search(selected_list, df)
        if preds:
            preds_df = pd.DataFrame(preds, columns=["Message", "Score", "Answer"])
            st.dataframe(preds_df)

            fname = f"Automated Responses - {datetime.datetime.now().isoformat()}.csv"
            st.download_button(
                label="Download data as CSV",
                data=preds_df.to_csv(index=False).encode(),
                file_name=fname,
            )
        else:
            st.markdown(":red[No rows selected.]")
