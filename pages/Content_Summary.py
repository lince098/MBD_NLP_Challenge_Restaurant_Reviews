import streamlit as st
from challenge_functions import general as g, openai_interface as oi
import asyncio
import pandas as pd
import datetime


st.sidebar.markdown("# Content Summary")
st.sidebar.markdown("Summarise the contents of chosen reviews.")

st.markdown("# Content Summary")


uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = g.load_csv_from_file_input(uploaded_file)

    with st.form("my_form"):
        st.markdown("### You can select the rows you want to analyze")

        st.dataframe(df)

        selected_list = st.multiselect("Index", df.index.to_list())

        submitted = st.form_submit_button("Get Summaries")

    if submitted:
        summaries = asyncio.run(oi.summarize(selected_list, df))

        if summaries:
            summaries_df = pd.DataFrame(summaries, columns=["Review", "Summary"])
            st.dataframe(summaries_df)
            fname = f"Summaries - {datetime.datetime.now().isoformat()}.csv"
            st.download_button(
                label="Download data as CSV",
                data=summaries_df.to_csv(index=False).encode(),
                file_name=fname,
            )
        else:
            st.markdown(":red[No rows selected.]")
