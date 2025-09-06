import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_silver_players(limit=20, pages=3):
    all_players = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, pages + 1):
        url = f"https://www.futbin.com/25/players?page={page}&version=silver_rare"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table#players tbody tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            try:
                name = cols[1].get_text(strip=True)
                rating = cols[2].get_text(strip=True)
                position = cols[3].get_text(strip=True)
                club = cols[4].get_text(strip=True)
                nation = cols[5].get_text(strip=True)
                ps_price_text = cols[7].get_text(strip=True).replace(",","").replace("€","").replace("K","000").replace("M","000000")
                ps_price = int(ps_price_text) if ps_price_text.isdigit() else 0

                all_players.append({
                    "Name": name,
                    "Rating": rating,
                    "Position": position,
                    "Club": club,
                    "Nation": nation,
                    "Preis (PS)": ps_price
                })
            except Exception:
                continue

    df = pd.DataFrame(all_players)
    df = df.sort_values("Preis (PS)", ascending=False).head(limit)
    return df

st.set_page_config(page_title="FC25 Silbermarkt PS", layout="wide")

st.title("💰 Teuerste Silber-Spieler in FC25 (PS Markt)")
st.caption("Datenquelle: Futbin (HTML Scraping, nur PS Preise, erste 3 Seiten)")

anzahl = st.slider("Anzahl Spieler anzeigen", 5, 100, 20)

df = get_silver_players(limit=anzahl, pages=3)
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV herunterladen", csv, "fc25_silver_ps.csv", "text/csv")