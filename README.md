# Que faire à Paris maintenant ?

Application web (Flask) qui propose les sorties culturelles à venir à Paris,
triées par distance, avec météo et lien d'itinéraire.
Données : Que faire à Paris (Ville de Paris, open data). Météo : Open-Meteo.

## Lancer avec Docker (recommandé)
```bash
docker build -t que-faire-paris .
docker run -p 5000:5000 que-faire-paris
```
Puis ouvrir http://localhost:5000
(au premier lancement, les données sont téléchargées et nettoyées automatiquement).

## Lancer sans Docker
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python telecharger.py   # télécharge data/evenements.csv
python clean.py         # produit data/evenements_propres.csv
python app.py           # http://localhost:5000
```

## Structure
- `telecharger.py` : téléchargement des données brutes
- `clean.py` : nettoyage (dates, coordonnées, colonnes utiles)
- `filtres.py` : filtres (date, thème, prix, intérieur/extérieur)
- `geo.py` : distances (Haversine)
- `meteo.py` : prévisions Open-Meteo avec cache
- `app.py` + `templates/` + `static/` : interface web

## Remarques
- Les résultats dépendent de la date du jour : seuls les événements à venir sont affichés.
- La photo d'accueil est `static/paris.jpg`.

Sous WSL avec Podman, si la page ne répond pas : `docker run -d --network host que-faire-paris`
Version de Python : 3.14

Sous WSL avec Podman, si la page ne répond pas : `docker run -d --network host que-faire-paris`
Version de Python : 3.14

## Récupérer le projet
```bash
git clone https://github.com/elfarfaraya-boop/application-paris.git
cd application-paris
```
