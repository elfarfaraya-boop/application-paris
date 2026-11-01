import numpy as np


def distance_km(lat1, lon1, lat2, lon2):
    """Distance à vol d'oiseau en km (formule de Haversine)."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return 6371 * 2 * np.arcsin(np.sqrt(a))


def centre_cp(df, cp):
    """Centre (lat, lon) des événements d'un code postal, ou None."""
    sous = df[df["address_zipcode"].astype(str).str.strip() == cp]
    if sous.empty:
        return None
    return float(sous["lat"].median()), float(sous["lon"].median())
