#!/bin/sh
# create config.ini file
echo "[DEFAULT]" > config.ini
echo "radarr_url = ${RADARR_URL}" >> config.ini
echo "radarr_api_key = ${RADARR_API}" >> config.ini
echo "trailer_folder = /trailers" >> config.ini
echo "interval = ${INTERVAL}" >> config.ini
# create an empty hidden file so Plex will delete all trailers from library if the folder is empty
touch /trailers/.placeholder
# launch app
python main.py