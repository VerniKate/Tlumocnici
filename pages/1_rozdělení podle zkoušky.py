import streamlit as st
from modules.data_loader import load_data
from modules.graphs import fig_pie2
import streamlit as st
from modules.data_loader import load_data
from modules.graphs import fig_pie2


st.set_page_config(page_title="Rozdělení podle zkoušky", layout="wide")
st.title("Rozdělení tlumočníků a překladatelů podle zkoušky")

df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grouped_roky, df_merged, df_jazyky_grouped = load_data()
jazyk = st.selectbox("Vyber jazyk", df_grouped['Jazyk'].unique())

fig = fig_pie2(df_grouped, jazyk)
st.plotly_chart(fig, use_container_width=True)




