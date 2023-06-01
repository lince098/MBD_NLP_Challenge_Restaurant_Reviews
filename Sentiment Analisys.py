import streamlit as st
from challenge_functions import sentiment_analysis as sa
from st_aggrid import GridOptionsBuilder, AgGrid, AgGridTheme
import pandas as pd
import datetime


def my_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(
        "multiple",
        use_checkbox=True,
    )  # Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode="AS_INPUT",
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=False,
        theme=AgGridTheme.STREAMLIT,
        enable_enterprise_modules=True,
        height=400,
        width="100%",
    )

    return grid_response


#
st.sidebar.markdown("# Sentiment Analysis")
st.sidebar.markdown(
    "Analyze the sentiment of the reviews, i.e., whether they are positive or negative."
)

st.markdown("# Sentiment Analysis")


uploaded_file = st.file_uploader("Insert a csv file with TripAdvisor reviews.")

if uploaded_file:
    df = sa.load_csv_from_file_input(uploaded_file)

    st.markdown("### You can select the rows you want to analyze")

    grid_response = my_aggrid(df)

    data = grid_response["data"]

    # Lista de diccionarios
    selected_list = grid_response["selected_rows"]

    show_predictions = False

    if "predictions" not in st.session_state:
        st.session_state["predictions"] = None

    if selected_list:
        st.button("Get predictions", on_click=lambda: sa.get_predictions(selected_list))

    else:
        st.button("Get predictions", disabled=True)
        st.session_state["predictions"] = None

    if st.session_state["predictions"]:
        data_out = [
            (selected["body"], pred["label"], pred["score"])
            for selected, pred in zip(selected_list, st.session_state["predictions"])
        ]

        result_df = pd.DataFrame(data_out, columns=["Review", "Label", "Score"])
        st.dataframe(result_df)

        fname = f"Sentiment Analysis - {datetime.datetime.now().isoformat()}.csv"
        st.download_button(
            label="Download data as CSV",
            data=result_df.to_csv(index=False).encode(),
            file_name=fname,
        )
