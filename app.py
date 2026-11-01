from flask import Flask, render_template, request
from filtres import charger, filtrer, lister_themes
from geo import distance_km, centre_cp
from meteo import charger_meteo, texte_meteo

app = Flask(__name__)
DF = charger()
THEMES = [t for t in lister_themes(DF).index if t != "Expo"]


def lien_itineraire(depart, lat, lon):
    """Lien Google Maps (transports en commun) vers l'événement."""
    url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=transit"
    if depart:
        url += f"&origin={depart[0]},{depart[1]}"
    return url


def en_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def lignes(d, meteo, depart=None, limite=100):
    """Transforme le tableau en liste simple pour la page."""
    out = []
    for _, r in d.head(limite).iterrows():
        dist = ""
        if "distance" in d.columns:
            dist = f"{r['distance']:.1f} km".replace(".", ",")
        out.append({
            "title": r["title"],
            "url": r["url"],
            "horaire": r["seance_debut"].strftime("%d/%m %H:%M"),
            "en_cours": bool(r["en_cours"]),
            "cp": "" if str(r["address_zipcode"]) == "nan" else r["address_zipcode"],
            "prix": r["price_type"],
            "distance": dist,
            "image": r["cover_url"] if isinstance(r["cover_url"], str) else "",
            "meteo": texte_meteo(meteo, r["a_partir_de"]),
            "exterieur": int(r["event_indoor"]) == 0,
            "itineraire": lien_itineraire(depart, r["lat"], r["lon"]),
        })
    return out


@app.route("/")
def index():
    prix = request.args.get("prix") or None
    lieu = request.args.get("lieu") or ""
    theme = request.args.get("theme") or None
    interieur = {"interieur": True, "exterieur": False}.get(lieu)

    lat = en_float(request.args.get("lat"))
    lon = en_float(request.args.get("lon"))
    cp = (request.args.get("cp") or "").strip()
    rayon_txt = request.args.get("rayon") or ""
    rayon = en_float(rayon_txt)

    origine = ""
    if cp:
        centre = centre_cp(DF, cp)
        if centre:
            lat, lon = centre
            origine = f"Centre du {cp}"
        else:
            origine = f"Code postal {cp} introuvable"
    if not origine and lat is not None and lon is not None:
        origine = "Ta position"
    avec_position = lat is not None and lon is not None
    depart = (lat, lon) if avec_position else None

    res = filtrer(DF, theme=theme, prix=prix, interieur=interieur)

    if not res.empty and avec_position:
        res = res.copy()
        res["distance"] = distance_km(lat, lon, res["lat"].values, res["lon"].values)
        if rayon:
            res = res[res["distance"] <= rayon]
        res = res.sort_values("distance")

    meteo = charger_meteo()

    sorties, expos = [], []
    nb_sorties = nb_expos = 0
    if not res.empty:
        est_expo = res["qfap_tags"].fillna("").str.contains("Expo", case=False, regex=False)
        nb_sorties, nb_expos = int((~est_expo).sum()), int(est_expo.sum())
        sorties = lignes(res[~est_expo], meteo, depart)
        expos = lignes(res[est_expo], meteo, depart)

    return render_template(
        "index.html", sorties=sorties, expos=expos,
        nb_sorties=nb_sorties, nb_expos=nb_expos,
        themes=THEMES, prix=prix or "", lieu=lieu, theme=theme or "",
        lat=lat if (avec_position and not cp) else "",
        lon=lon if (avec_position and not cp) else "",
        cp=cp, rayon=rayon_txt, origine=origine,
    )


if __name__ == "__main__":
    app.run(debug=True)
