import streamlit as st
from challenge_functions import answer_reviews as ar, general as g

st.sidebar.markdown("# Automated Responses")

st.markdown("# Automated Responses")
st.sidebar.markdown(
    "Automate responses for your reviews. Given a dataset, this feature will let you download a csv with the best answer for each review."
)

uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = g.load_csv_from_file_input(uploaded_file)
    st.dataframe(df)