import streamlit as st
from modules.data_loader import load_data
from modules.graphs import fig_bar

st.set_page_config(page_title="Města s nejvíce tlumočníky/překladateli", layout="wide")
st.title("Počet měst s více než 20 tlumočníky/překladateli")

# Načtení dat
df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grouped_roky, df_merged, df_jazyky_grouped = load_data()


# Debug výpis (volitelně)
# st.write("Sloupce v df_grouped_jazyky:", df_grouped_jazyky.columns.tolist())
# st.dataframe(df_grouped_jazyky)

# Vykreslení grafu
from modules.graphs import fig_line2

fig = fig_line2(df_filtered_mesta)
st.plotly_chart(fig, use_container_width=True)