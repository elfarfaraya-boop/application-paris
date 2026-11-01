import pandas as pd

df = pd.read_csv("data/evenements.csv", sep=";")
print("Lignes au départ :", len(df))

# 1. Dates : conversion en heure de Paris
for c in ["date_start", "date_end"]:
    df[c] = pd.to_datetime(df[c], utc=True, errors="coerce").dt.tz_convert("Europe/Paris")

# 2. Coordonnées : séparer lat_lon, traiter 0.0 comme manquant
coords = df["lat_lon"].str.split(",", expand=True)
df["lat"] = pd.to_numeric(coords[0], errors="coerce")
df["lon"] = pd.to_numeric(coords[1], errors="coerce")
df.loc[(df["lat"] == 0) | (df["lon"] == 0), ["lat", "lon"]] = float("nan")

# 3. Supprimer les lignes inutilisables
df = df.dropna(subset=["date_end", "lat", "lon"])
print("Après suppression des dates/coordonnées manquantes :", len(df))

# 4. Garder les événements pas encore terminés
now = pd.Timestamp.now(tz="Europe/Paris")
df = df[df["date_end"] >= now]
print("Événements à venir ou en cours :", len(df))

# 5. Colonnes utiles
cols = ["id", "title", "lead_text", "url", "date_start", "date_end",
        "date_description", "occurrences", "address_name", "address_street",
        "address_zipcode", "lat", "lon", "cover_url", "price_type", "qfap_tags", "event_indoor"]
df = df[cols].sort_values("date_start")

df.to_csv("data/evenements_propres.csv", index=False)
print("Fichier écrit : data/evenements_propres.csv")
print("Première date de fin :", df["date_end"].min())
print("Dernière date de fin :", df["date_end"].max())
