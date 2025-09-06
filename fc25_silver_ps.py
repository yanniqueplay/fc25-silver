import requests
import pandas as pd
import streamlit as st

def get_silver_players(limit=20):
    url = "https://www.fut.gg/api/players/"
    params = {
        "rarity": "silver",
        "platform": "ps",
        "limit": limit,
        "sort": "price",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

st.set_page_config(page_title="Teuerste Silber-Spieler in FC25 (PS)", layout="wide")

st.title("💰 Teuerste Silber-Spieler in EA FC 25 (PS Markt)")
st.caption("Datenquelle: [FUT.GG](https://www.fut.gg)")

anzahl = st.slider("Anzahl der Spieler anzeigen", 5, 100, 20)

players = get_silver_players(limit=anzahl)

df = pd.DataFrame(players)
df = df[["name", "rating", "position", "club", "nation", "price"]]
df.columns = ["Name", "Bewertung", "Position", "Verein", "Nation", "Preis (PS)"]

st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV herunterladen", csv, "fc25_silver_ps.csv", "text/csv")