#!/bin/sh
echo "[DEFAULT]" > config.ini
echo "radarr_url = ${RADARR_URL}" >> config.ini
echo "tmdb_api_key = ${TMDB_API}" >> config.ini
echo "radarr_api_key = ${RADARR_API}" >> config.ini
echo "language = ${LANG}" >> config.ini
echo "country = ${COUNTRY}" >> config.ini
echo "trailer_folder = /trailers" >> config.ini
echo "interval = ${INTERVAL}" >> config.ini

python main.py &