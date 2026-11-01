import json
import os
import time

import requests

URL = "https://api.open-meteo.com/v1/forecast"
CACHE = "data/meteo_cache.json"
DUREE_CACHE = 3600  # 1 heure
PARIS_LAT, PARIS_LON = 48.8566, 2.3522


def _telecharger():
    r = requests.get(URL, params={
        "latitude": PARIS_LAT,
        "longitude": PARIS_LON,
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        "timezone": "Europe/Paris",
        "forecast_days": 8,
    }, timeout=10)
    r.raise_for_status()
    return r.json()["hourly"]


def charger_meteo():
    """Prévisions horaires, avec cache. Renvoie {heure: (temp, pluie %, code)}."""
    data = None
    cache_frais = (os.path.exists(CACHE)
                   and time.time() - os.path.getmtime(CACHE) < DUREE_CACHE)
    if not cache_frais:
        try:
            data = _telecharger()
            with open(CACHE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print("Météo indisponible :", e)
    if data is None and os.path.exists(CACHE):  # cache (même ancien) en secours
        with open(CACHE) as f:
            data = json.load(f)
    if data is None:
        return {}
    return {
        t: (temp, pluie, code)
        for t, temp, pluie, code in zip(
            data["time"], data["temperature_2m"],
            data["precipitation_probability"], data["weather_code"])
    }


def icone(code):
    if code is None:
        return ""
    if code == 0:
        return "☀️"
    if code in (1, 2):
        return "🌤️"
    if code == 3:
        return "☁️"
    if code in (45, 48):
        return "🌫️"
    if code in (51, 53, 55, 56, 57):
        return "🌦️"
    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "🌧️"
    if code in (71, 73, 75, 77, 85, 86):
        return "❄️"
    if code in (95, 96, 99):
        return "⛈️"
    return ""


def texte_meteo(meteo, moment):
    """Texte du genre '☁️ 12° · pluie 40%' pour un moment donné, ou ''."""
    cle = moment.floor("h").strftime("%Y-%m-%dT%H:00")
    if cle not in meteo:
        return ""
    temp, pluie, code = meteo[cle]
    if temp is None:
        return ""
    txt = f"{icone(code)} {round(temp)}°"
    if pluie is not None:
        txt += f" · pluie {pluie}%"
    return txt
