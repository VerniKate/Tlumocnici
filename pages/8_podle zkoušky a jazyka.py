import streamlit as st
from modules.data_loader import load_data
from modules.graphs import fig_bar_stacked


st.set_page_config(page_title="Rozdělení podle zkoušky a jazyka", layout="wide")
st.title("Rozdělení tlumočníků a překladatelů podle zkoušky a jazyka")

df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grouped_roky, df_merged, df_jazyky_grouped = load_data()


fig = fig_bar_stacked(df_grouped)
st.plotly_chart(fig, use_container_width=True)
