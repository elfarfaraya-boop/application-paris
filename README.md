# Que faire à Paris maintenant ?

Application web (Flask) qui propose les sorties culturelles à venir à Paris,
triées par distance, avec la météo prévue et un lien d'itinéraire.

- Données : « Que faire à Paris » (Ville de Paris, open data)
- Météo : Open-Meteo
- Python : 3.14

## Récupérer le projet

    git clone https://github.com/elfarfaraya-boop/application-paris.git
    cd application-paris

(ou télécharger le zip depuis GitHub, l'extraire et ouvrir un terminal dans le dossier)

## Lancer avec Docker ou Podman (recommandé)

    docker build -t que-faire-paris .
    docker run -p 5000:5000 que-faire-paris

Puis ouvrir http://localhost:5000.
Au premier lancement, les données sont téléchargées et nettoyées automatiquement
(environ 30 secondes). Une connexion Internet est nécessaire.

Sous WSL avec Podman, si la page ne répond pas :

    docker run -d --network host que-faire-paris

Pour arrêter : `docker stop $(docker ps -q)`

## Lancer sans Docker

    python3 -m venv .venv
    source .venv/bin/activate        # Windows : .venv\Scripts\activate
    pip install -r requirements.txt
    python telecharger.py            # télécharge data/evenements.csv
    python clean.py                  # produit data/evenements_propres.csv
    python app.py                    # http://localhost:5000

## Structure

- `telecharger.py` : téléchargement des données brutes
- `clean.py` : nettoyage (dates, coordonnées, colonnes utiles)
- `filtres.py` : filtres (date, thème, prix, intérieur/extérieur)
- `geo.py` : distances à vol d'oiseau (Haversine)
- `meteo.py` : prévisions Open-Meteo avec cache
- `app.py`, `templates/`, `static/` : interface web
- `outils/` : scripts d'exploration des données
- `Dockerfile`, `start.sh` : exécution reproductible

## Remarques

- Les données changent chaque jour : les événements affichés dépendent de la date
  d'exécution (seuls les événements à venir sont gardés).
- La distance est calculée à vol d'oiseau ; l'itinéraire ouvre Google Maps.
- La photo d'accueil est `static/paris.jpg`.
