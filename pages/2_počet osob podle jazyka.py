import streamlit as st
from modules.data_loader import load_data
from modules.graphs import fig_bar

st.set_page_config(page_title="Tlumočníci podle jazyka", layout="wide")
st.title("Počet tlumočníků/překladatelů podle jazyka a druhu osoby")

# Načtení dat
df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grpuped_roky, df_merged, df_jazyky_grouped = load_data()

# Debug výpis (volitelně)
# st.write("Sloupce v df_grouped_jazyky:", df_grouped_jazyky.columns.tolist())
# st.dataframe(df_grouped_jazyky)

# Vykreslení grafu
fig = fig_bar(df_grouped_jazyky)
st.plotly_chart(fig, use_container_width=True)
