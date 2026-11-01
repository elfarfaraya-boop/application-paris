#!/bin/sh
set -e
if [ ! -f data/evenements_propres.csv ]; then
  python telecharger.py
  python clean.py
fi
exec gunicorn -b 0.0.0.0:${PORT:-5000} app:app
