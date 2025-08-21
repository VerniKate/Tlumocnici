import streamlit as st
from modules.data_loader import load_data
from modules.graphs import line_chart_grouped_roky
from modules.graphs import create_cumulative_graph
from modules.graphs import scatter_chart_jazyky

# Načtení dat
df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grouped_roky, df_merged, df_jazyky_grouped = load_data()

# Titulek stránky
st.title("Počet nově zapsaných v jednotlivých letech podle průměrného počtu zapsaných jazyků")

# Vykreslení grafu
fig = scatter_chart_jazyky(df_merged)
st.plotly_chart(fig, use_container_width=True)