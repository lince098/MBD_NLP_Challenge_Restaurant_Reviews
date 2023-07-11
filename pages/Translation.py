import streamlit as st
from challenge_functions import general as g, openai_interface as oi
import asyncio
import pandas as pd
import datetime

LANGUAGES = [
    "English",
    "Mandarin",
    "Hindi",
    "Spanish",
    "French",
    "Arabic",
    "Bengali",
    "Russian",
    "Portuguese",
]

st.sidebar.markdown("# Translation")
st.sidebar.markdown("Translate to any of the chosen languages the reviews.")

st.markdown("# Translation")


uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = g.load_csv_from_file_input(uploaded_file)

    with st.form("my_form"):
        st.markdown("### You can select the rows you want to analyze")

        st.dataframe(df)

        selected_list = st.multiselect("Index", df.index.to_list())

        language = st.selectbox("Target language to translate:", LANGUAGES)

        submitted = st.form_submit_button("Get Translations")

    if submitted:
        summaries = asyncio.run(oi.get_translations(selected_list, df, language))

        if summaries:
            summaries_df = pd.DataFrame(summaries, columns=["Review", "Translation"])
            st.dataframe(summaries_df)
            fname = f"Translations - {datetime.datetime.now().isoformat()}.csv"
            st.download_button(
                label="Download data as CSV",
                data=summaries_df.to_csv(index=False).encode(),
                file_name=fname,
            )
        else:
            st.markdown(":red[No rows selected.]")
