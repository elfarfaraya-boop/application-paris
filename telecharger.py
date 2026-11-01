import os
import requests

URL = ("https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/"
       "que-faire-a-paris-/exports/csv?delimiter=%3B")

os.makedirs("data", exist_ok=True)
r = requests.get(URL, timeout=120)
r.raise_for_status()
with open("data/evenements.csv", "wb") as f:
    f.write(r.content)
print("OK :", len(r.content) // 1024, "Ko téléchargés")
