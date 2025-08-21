import os
import pandas as pd

def load_data():
    # Cesta k souboru CSV
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "df_aktivni_vybrane_sloupce.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Soubor nebyl nalezen: {file_path}")

    # Načtení dat
    df = pd.read_csv(file_path)

    # Zpracování jazyků
    df['Jazyky'] = df['Jazyky'].fillna('')
    df['Jazyky_list'] = df['Jazyky'].str.split('|')
    df['Počet jazyků'] = df['Jazyky_list'].apply(len)
    df = df.explode('Jazyky_list')
    df['Jazyk'] = df['Jazyky_list'].str.strip()
    df.drop(columns='Jazyky_list', inplace=True)

    # Vytvoření identifikátoru osoby
    df['Identita'] = (
        df['Jméno'].fillna('') + "_" +
        df['Příjmení'].fillna('') + "_" +
        df['Rok zápisu'].astype(str)
    )

    # 1️⃣ Počet osob podle zkoušky, druhu osoby a jazyka
    df_grouped = (
        df.groupby(['Zkouška vykonána', 'Druh osoby', 'Jazyk'])['Identita']
        .nunique()
        .reset_index()
        .rename(columns={'Identita': 'Počet osob'})
    )

    # 2️⃣ Počet osob podle jazyka
    df_jazyk_count = (
        df.groupby('Jazyk')['Identita']
        .nunique()
        .reset_index()
        .rename(columns={'Identita': 'Počet'})
    )

    # 3️⃣ Počet tlumočníků/překladatelů podle druhu osoby a jazyka
    df_grouped_jazyky = (
        df.groupby(['Druh osoby', 'Jazyk'])['Identita']
        .nunique()
        .reset_index()
        .rename(columns={'Identita': 'Počet tlumočníků/překladatelů'})
    )
    df_grouped_mesta = df.groupby(['Město', 'Druh osoby'])['Identita'].nunique().reset_index()
    df_grouped_mesta.columns = ['Město', 'Druh osoby', 'Počet tlumočníků/překladatelů']

    # Filter for cities with more than 20 tlumočníků/překladatelů
    df_filtered_mesta = df_grouped_mesta[df_grouped_mesta['Počet tlumočníků/překladatelů'] > 20]

    df_grouped_roky = df.groupby(['Rok zápisu', 'Druh osoby'])['Identita'].nunique().reset_index()
    df_grouped_roky.columns = ['Rok zápisu', 'Druh osoby', 'Počet osob']

    # Calculate cumulative count for each 'Druh osoby'
    df_grouped_roky['Kumulativní počet'] = df_grouped_roky.groupby('Druh osoby')['Počet osob'].cumsum()

    df_avg_languages = df.groupby(['Rok zápisu', 'Druh osoby'])['Počet jazyků'].mean().reset_index()
    df_avg_languages.columns = ['Rok zápisu', 'Druh osoby', 'Průměrný počet jazyků']

    # Sloučení s agregovanými daty o počtu osob
    df_merged = pd.merge(df_grouped_roky, df_avg_languages, on=['Rok zápisu', 'Druh osoby'])

    df_jazyky_grouped = df.groupby(['Rok zápisu', 'Jazyk']).size().reset_index(name='Počet osob')
    return df_grouped, df_jazyk_count, df_grouped_jazyky, df_filtered_mesta, df_grouped_roky, df_merged, df_jazyky_grouped