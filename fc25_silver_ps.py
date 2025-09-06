import requests
import pandas as pd
import streamlit as st

def get_silver_players(limit=20, pages=3):
    all_players = []

    for page in range(1, pages + 1):
        url = f"https://www.futbin.com/25/players?page={page}&version=silver_rare"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        for p in data["items"]:
            ps_price = p.get("ps_price", 0) or 0
            all_players.append({
                "Name": p.get("name"),
                "Rating": p.get("rating"),
                "Position": p.get("position"),
                "Club": p.get("club_name"),
                "Nation": p.get("nation_name"),
                "Preis (PS)": ps_price
            })

    df = pd.DataFrame(all_players)
    df = df.sort_values("Preis (PS)", ascending=False).head(limit)

    return df

st.set_page_config(page_title="FC25 Silbermarkt PS", layout="wide")

st.title("💰 Teuerste Silber-Spieler in FC25 (PS Markt)")
st.caption("Datenquelle: Futbin API (live Preise, nur PS, erste 3 Seiten)")

anzahl = st.slider("Anzahl Spieler anzeigen", 5, 100, 20)

df = get_silver_players(limit=anzahl, pages=3)
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV herunterladen", csv, "fc25_silver_ps.csv", "text/csv")