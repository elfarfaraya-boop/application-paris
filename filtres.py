import pandas as pd

PARIS = "Europe/Paris"


def charger():
    """Charge le fichier propre et remet les dates en heure de Paris."""
    df = pd.read_csv("data/evenements_propres.csv")
    for c in ["date_start", "date_end"]:
        df[c] = pd.to_datetime(df[c], utc=True).dt.tz_convert(PARIS)
    return df


def lister_themes(df):
    """Liste tous les thèmes présents dans qfap_tags (séparés par ';')."""
    themes = df["qfap_tags"].dropna().str.split(";").explode().str.strip()
    return themes.value_counts()


def seances(ligne):
    """Renvoie la liste des (début, fin) d'un événement, en heure de Paris."""
    occ = ligne["occurrences"]
    res = []
    if isinstance(occ, str) and occ.strip():
        for morceau in occ.split(";"):
            try:
                d, f = morceau.split("_")
                res.append((pd.Timestamp(d).tz_convert(PARIS),
                            pd.Timestamp(f).tz_convert(PARIS)))
            except (ValueError, TypeError):
                continue
    if not res:  # pas d'occurrences : on retombe sur la plage globale
        res = [(ligne["date_start"], ligne["date_end"])]
    return res


def prochaine_seance(ligne, debut, fin, garder_longues, max_heures):
    """Première séance qui chevauche [debut, fin], ou None."""
    for d, f in sorted(seances(ligne)):
        if f < debut or d > fin:
            continue
        duree_h = (f - d).total_seconds() / 3600
        if not garder_longues and duree_h > max_heures:
            continue
        return d, f
    return None


def filtrer(df, debut=None, fin=None, theme=None, exclure_theme=None,
            prix=None, interieur=None, garder_longues=False, max_heures=24):
    """
    debut          : début de la fenêtre (par défaut : maintenant).
    fin            : fin de la fenêtre (par défaut : début + 7 jours).
    theme          : texte à chercher dans qfap_tags (ex. "Concert").
    exclure_theme  : thème à écarter (ex. "Expo").
    prix           : "gratuit", "payant" ou None.
    interieur      : True, False ou None.
    garder_longues : True pour inclure les séances très longues.
    max_heures     : durée max d'une séance "ponctuelle" (24 h par défaut).
    """
    maintenant = pd.Timestamp.now(tz=PARIS)
    debut = maintenant if debut is None else max(debut, maintenant)
    fin = debut + pd.Timedelta(days=7) if fin is None else fin

    res = df
    if theme:
        res = res[res["qfap_tags"].fillna("").str.contains(theme, case=False, regex=False)]
    if exclure_theme:
        res = res[~res["qfap_tags"].fillna("").str.contains(exclure_theme, case=False, regex=False)]
    if prix:
        res = res[res["price_type"] == prix]
    if interieur is not None:
        res = res[res["event_indoor"] == (1 if interieur else 0)]

    res = res.copy()
    if res.empty:
        return res

    prochaines = res.apply(
        lambda l: prochaine_seance(l, debut, fin, garder_longues, max_heures), axis=1
    )
    res = res[prochaines.notna()].copy()
    prochaines = prochaines[prochaines.notna()]
    res["seance_debut"] = [p[0] for p in prochaines]
    res["seance_fin"] = [p[1] for p in prochaines]

    # Ce qu'on peut faire "à partir de maintenant"
    res["en_cours"] = res["seance_debut"] <= debut
    res["a_partir_de"] = res["seance_debut"].where(~res["en_cours"], debut)
    return res.sort_values(["a_partir_de", "seance_debut"])


if __name__ == "__main__":
    df = charger()
    res = filtrer(df, prix="gratuit", exclure_theme="Expo")
    print(f"Gratuit, hors expos, 7 prochains jours : {len(res)} événements")
    print(res[["title", "seance_debut", "en_cours", "address_zipcode"]].head(15).to_string())
