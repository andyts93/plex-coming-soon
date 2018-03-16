import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/lib')
from tmdb3 import set_key, set_locale, Movie

set_key('bee608b6e6519d689c39001fb805090a')
set_locale('it', 'it')

def get_trailers(imdb_id):
	movie = Movie(imdb_id)
	if movie:
		trailers = movie.youtube_trailers
		if not trailers:
			# try to get english trailer
			set_locale('en', 'gb')
			return get_trailers(imdb_id)
		else:
			set_locale('it', 'it')
			return trailers

def get_history():
	url = "http://192.168.0.20:7878/api/history?page=1&pageSize=10&apikey=326cc12ace3c496791d11f8630ca60f3"
	response = requests.get(url).json()
	if 'error' in response:
		raise Exception(response['error'])
	if response['totalRecords'] == 0:
		print "No entry in radarr history"
	else:
		grabbed = [x for x in response['records'] if x['eventType'] == 'grabbed' and x['movie']['hasFile'] == False]
		if not grabbed:
			print "No coming soon titles"
		else:
			for item in grabbed:
				if 'movie' in item and 'tmdbId' in item['movie']:
					trailers = get_trailers(item['movie']['tmdbId'])
					print trailers

try:
	get_history()
except Exception as e:
	print(e);

# def parseRSS(rss_url):
# 	return feedparser.parse(rss_url)

# def purge_dir(dir):
# 	for f in os.listdir(dir):
# 		os.remove(os.path.join(dir, f))

		

