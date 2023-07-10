import streamlit as st
from challenge_functions import general as g
from challenge_functions.star_distribution import get_ratings_barplot

st.sidebar.markdown("# Stars Distribution")
st.sidebar.markdown("Shows a barplot of the ratings in the data.")

st.markdown("# Stars Distribution")

uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = g.load_csv_from_file_input(uploaded_file)
    st.dataframe(df)
    fig, ax = get_ratings_barplot(df)
    st.pyplot(fig)
