import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def fig_pie2(df_grouped, jazyk):
    # Filtrování dat pro vybraný jazyk
    df_filtered = df_grouped[df_grouped['Jazyk'] == jazyk]

    # Celková agregace bez ohledu na jazyk
    df_total = df_grouped

    # Agregace pro tlumočníky – jazykově specifické
    tlumočníci_jazyk = (
        df_filtered[df_filtered['Druh osoby'] == 'Soudní tlumočník']
        .groupby('Zkouška vykonána')['Počet osob']
        .sum()
        .reindex(['Ano', 'Ne'], fill_value=0)
    )

    # Agregace pro překladatele – jazykově specifické
    překladatelé_jazyk = (
        df_filtered[df_filtered['Druh osoby'] == 'Soudní překladatel']
        .groupby('Zkouška vykonána')['Počet osob']
        .sum()
        .reindex(['Ano', 'Ne'], fill_value=0)
    )

    # Agregace pro tlumočníky – celkové
    tlumočníci_total = (
        df_total[df_total['Druh osoby'] == 'Soudní tlumočník']
        .groupby('Zkouška vykonána')['Počet osob']
        .sum()
        .reindex(['Ano', 'Ne'], fill_value=0)
    )

    # Agregace pro překladatele – celkové
    překladatelé_total = (
        df_total[df_total['Druh osoby'] == 'Soudní překladatel']
        .groupby('Zkouška vykonána')['Počet osob']
        .sum()
        .reindex(['Ano', 'Ne'], fill_value=0)
    )

    # Vytvoření 4 koláčových grafů vedle sebe
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'domain'}, {'type': 'domain'}],
               [{'type': 'domain'}, {'type': 'domain'}]],
        subplot_titles=[
            f'Tlumočníci – {jazyk}', f'Překladatelé – {jazyk}',
            'Tlumočníci – celkem', 'Překladatelé – celkem'
        ]
    )

    # Tlumočníci – jazyk
    fig.add_trace(go.Pie(
        labels=tlumočníci_jazyk.index,
        values=tlumočníci_jazyk.values,
        name='Tlumočníci – jazyk',
        marker=dict(colors=['#2ca02c', '#98df8a']),
        hole=0.4
    ), row=1, col=1)

    # Překladatelé – jazyk
    fig.add_trace(go.Pie(
        labels=překladatelé_jazyk.index,
        values=překladatelé_jazyk.values,
        name='Překladatelé – jazyk',
        marker=dict(colors=['#1f77b4', '#aec7e8']),
        hole=0.4
    ), row=1, col=2)

    # Tlumočníci – celkem
    fig.add_trace(go.Pie(
        labels=tlumočníci_total.index,
        values=tlumočníci_total.values,
        name='Tlumočníci – celkem',
        marker=dict(colors=['#2ca02c', '#98df8a']),
        hole=0.4
    ), row=2, col=1)

    # Překladatelé – celkem
    fig.add_trace(go.Pie(
        labels=překladatelé_total.index,
        values=překladatelé_total.values,
        name='Překladatelé – celkem',
        marker=dict(colors=['#1f77b4', '#aec7e8']),
        hole=0.4
    ), row=2, col=2)

    # Vzhled a anotace
    fig.update_layout(
        title_text=f"Rozdělení podle vykonané zkoušky – jazyk: {jazyk} a celkově",
        showlegend=False,
        template='plotly_white'
    )

    return fig

import plotly.graph_objects as go

import plotly.graph_objects as go

import plotly.graph_objects as go

def fig_bar(df):
    fig = go.Figure()

    # Automatické hledání sloupce s počtem tlumočníků/překladatelů
    target_col = None
    for col in df.columns:  # ✅ Oprava tady: používáme parametr df, ne df_grouped
        if "Počet" in col and ("tlumočníků" in col or "překladatelů" in col):
            target_col = col
            break

    if not target_col:
        print("Dostupné sloupce:", df.columns.tolist())
        raise ValueError("Sloupec s počtem tlumočníků/překladatelů nebyl nalezen.")

    for osoba in df['Druh osoby'].unique():
        df_filtered = df[df['Druh osoby'] == osoba]
        fig.add_trace(
            go.Bar(
                x=df_filtered['Jazyk'],
                y=df_filtered[target_col],
                name=osoba
            )
        )

    fig.update_layout(
        title='Počet tlumočníků/překladatelů podle jazyka',
        xaxis_title='Jazyk',
        yaxis_title='Počet osob',
        legend_title='Druh osoby',
        xaxis_tickangle=-45,
        template='plotly_white',
        barmode='group'
    )

    return fig

import streamlit as st
import plotly.graph_objects as go

def fig_line2(df):
    fig_line2 = go.Figure()

# Přidání jednotlivých linií pro každý druh osoby
    for osoba in df['Druh osoby'].unique():
        df_osoba = df[df['Druh osoby'] == osoba]
        fig_line2.add_trace(
            go.Scatter(
                x=df_osoba['Město'],
                y=df_osoba['Počet tlumočníků/překladatelů'],
                mode='lines+markers',
                name=osoba
             )
        )

# Nastavení vzhledu grafu
    fig_line2.update_layout(
        title='Počet měst s více než 20 tlumočníky/překladateli',
        xaxis_title='Město',
        yaxis_title='Počet osob',
        legend_title='Druh osoby',
        xaxis_tickangle=-45,
        template='plotly_white'
    )
    return fig_line2

import plotly.graph_objects as go

def fig_line3(df):
    fig = go.Figure()

    # Přidání jednotlivých linií pro každý druh osoby
    for osoba in df['Druh osoby'].unique():
        df_osoba = df[df_grouped_roky['Druh osoby'] == osoba]
        fig.add_trace(
            go.Scatter(
                x=df_osoba['Rok zápisu'],
                y=df_osoba['Kumulativní počet'],
                mode='lines+markers',
                name=osoba,
                marker=dict(size=6),
                line=dict(width=2),
                hovertemplate=f'Druh osoby: {osoba}<br>Rok: %{{x}}<br>Kumulativní počet: %{{y}}<extra></extra>'
            )
        )

    # Nastavení vzhledu grafu
    fig.update_layout(
        title='Kumulativní zapsaných tlumočníků/překladatelů v průběhu let',
        xaxis_title='Rok zápisu',
        yaxis_title='Kumulativní počet osob',
        legend_title='Druh osoby',
        template='plotly_white',
        hovermode='x unified'
    )

    return fig

import plotly.graph_objects as go

def create_cumulative_graph(df):
    fig = go.Figure()
    for osoba in df['Druh osoby'].unique():
        df_osoba = df[df['Druh osoby'] == osoba]
        fig.add_trace(
            go.Scatter(
                x=df_osoba['Rok zápisu'],
                y=df_osoba['Kumulativní počet'],
                mode='lines+markers',
                name=osoba,
                marker=dict(size=6),
                line=dict(width=2),
                hovertemplate=f'Druh osoby: {osoba}<br>Rok: %{{x}}<br>Kumulativní počet: %{{y}}<extra></extra>'
            )
        )
    fig.update_layout(
        title='Kumulativní zapsaných tlumočníků/překladatelů v průběhu let',
        xaxis_title='Rok zápisu',
        yaxis_title='Kumulativní počet osob',
        legend_title='Druh osoby',
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

import plotly.graph_objects as go

def line_chart_grouped_roky(df):
    """
    Vytvoří lineární graf počtu nově zapsaných osob podle druhu osoby a roku zápisu.

    Parameters:
    - df_grouped_roky: DataFrame s sloupci 'Druh osoby', 'Rok zápisu', 'Počet osob'

    Returns:
    - fig: Objekt grafu typu plotly.graph_objects.Figure
    """
    fig = go.Figure()

    # Přidání jednotlivých linií pro každý druh osoby
    for osoba in df['Druh osoby'].unique():
        df_osoba = df[df['Druh osoby'] == osoba]
        fig.add_trace(
            go.Scatter(
                x=df_osoba['Rok zápisu'],
                y=df_osoba['Počet osob'],
                mode='lines+markers',
                name=osoba,
                marker=dict(size=6),
                line=dict(width=2),
                hovertemplate=f'Druh osoby: {osoba}<br>Rok: %{{x}}<br>Počet: %{{y}}<extra></extra>'
            )
        )

    # Nastavení vzhledu grafu
    fig.update_layout(
        title='Počet nově zapsaných tlumočníků/překladatelů v jednotlivých letech',
        xaxis_title='Rok zápisu',
        yaxis_title='Počet osob',
        legend_title='Druh osoby',
        template='plotly_white',
        hovermode='x unified'
    )

    return fig

import plotly.graph_objects as go

def scatter_chart_jazyky(df):
    """
    Vytvoří scatter graf nově zapsaných osob podle roku a průměrného počtu jazyků.

    Parameters:
    - df_merged: DataFrame s sloupci 'Rok zápisu', 'Počet osob', 'Průměrný počet jazyků', 'Druh osoby'

    Returns:
    - fig: Objekt grafu typu plotly.graph_objects.Figure
    """
    fig = go.Figure()

    for osoba in df['Druh osoby'].unique():
        df_osoba = df[df['Druh osoby'] == osoba]

        fig.add_trace(
            go.Scatter(
                x=df_osoba['Rok zápisu'],
                y=df_osoba['Počet osob'],
                mode='markers',
                name=osoba,
                marker=dict(
                    size=10,
                    color=df_osoba['Průměrný počet jazyků'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Průměrný počet jazyků')
                ),
                hovertemplate=(
                    f'Druh osoby: {osoba}<br>'
                    'Rok: %{x}<br>'
                    'Počet osob: %{y}<br>'
                    'Průměrný počet jazyků: %{marker.color:.2f}<extra></extra>'
                )
            )
        )

    fig.update_layout(
        title='Počet nově zapsaných v jednotlivých letech podle průměrného počtu jazyků',
        xaxis_title='Rok zápisu',
        yaxis_title='Počet osob',
        legend_title='Druh osoby',
        legend=dict(
            x=0.5,
            y=1,
            xanchor='center',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1
        ),
        template='plotly_white',
        hovermode='closest'
    )

    return fig

import plotly.express as px

def bar_chart_jazyky_animace(df_jazyky_grouped):
    """
    Vytvoří animovaný bar chart zobrazující počet osob podle jazyka v jednotlivých letech.

    Parameters:
    - df_jazyky_grouped: DataFrame s sloupci 'Jazyk', 'Počet osob', 'Rok zápisu'

    Returns:
    - fig: Objekt grafu typu plotly.express.Figure
    """
    fig = px.bar(
        df_jazyky_grouped,
        x='Jazyk',
        y='Počet osob',
        color='Jazyk',
        animation_frame='Rok zápisu',
        title='Počet zapsaných osob podle jazyka v jednotlivých letech',
        labels={'Počet osob': 'Počet osob', 'Jazyk': 'Jazyk'}
    )

    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=10)
        )
    )

    return fig

import plotly.express as px

def fig_bar_stacked(df_grouped):
    fig = px.bar(
        df_grouped,
        x='Jazyk',
        y='Počet osob',
        color='Zkouška vykonána',
        pattern_shape='Druh osoby',  # volitelné: odliší typ osoby vzorem
        barmode='stack',
        labels={
            'Jazyk': 'Jazyk',
            'Počet osob': 'Počet',
            'Zkouška vykonána': 'Zkouška',
            'Druh osoby': 'Typ osoby'
        },
        title='Složená vs. nesložená zkouška podle jazyka a typu osoby'
    )

    fig.update_layout(
        template='plotly_white',
        height=600,
        legend_title='Zkouška vykonána'
    )

    return fig