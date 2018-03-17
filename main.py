from __future__ import unicode_literals
import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/lib')
from tmdb3 import set_key, set_locale, Movie, set_cache
import youtube_dl
import re
import unicodedata
import shutil
from ConfigParser import SafeConfigParser
import time
from logger import debug, info, warning, error, critical, logger

# get config file
parser = SafeConfigParser()
found = parser.read(os.path.dirname(__file__)+'/config.ini')
if not found:
	critical("Configuration file not found, check your config.ini file")
	exit()

main_folder = parser.get('DEFAULT', 'trailer_folder')

# set tmdb api key
try:
	set_key(parser.get('DEFAULT', 'tmdb_api_key'))
except Exception as e:
	critical(e)
	exit()

set_locale(parser.get('DEFAULT', 'language'), parser.get('DEFAULT', 'country'))

def yt_hook(d):
	if d['status'] == 'finished':
		info('File downloaded in %s' % (d['filename']))

# youtube-dl options
ydl_opts = {
	'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
	'ignoreerrors': True,
	'no_warnings': True,
	'logger': logger,
	'verbose': False,
	'progress_hooks': [yt_hook],
	"simulate": True
}

def get_trailers(tmdbId, retry):
	try:
		debug("Searching for movie with id %d" % (tmdbId))
		movie = Movie(tmdbId)
		if movie:
			trailers = movie.youtube_trailers
			if not trailers and retry == True:
				# try to get english trailer
				set_locale('en', 'gb')
				return get_trailers(tmdbId, False)
			else:
				set_locale(parser.get('DEFAULT', 'language'), parser.get('DEFAULT', 'country'))
				return trailers
	except Exception as e:
		if str(e) == '25':
			info("API limit reached, sleep for 10 seconds")
			time.sleep(10)
			return get_trailers(tmdbId, retry)


def has_trailer(foldername):
	return os.path.exists(main_folder+'/'+foldername)

def get_history():
	url = "http://192.168.0.20:7878/api/history?page=1&pageSize=100&apikey="+parser.get('DEFAULT', 'radarr_api_key')
	response = requests.get(url).json()
	if 'error' in response:
		raise Exception(response['error'])
	if response['totalRecords'] == 0:
		info("No entry in radarr history")
	else:
		grabbed = [x for x in response['records'] if x['eventType'] == 'grabbed']
		if not grabbed:
			info("No coming soon movies")
		else:
			for item in grabbed:
				if 'movie' in item:
					foldername = "%s (%d)" % (item['movie']['title'], item['movie']['year'])
					if 'tmdbId' in item['movie'] and item['movie']['hasFile'] == False:
						if not has_trailer(foldername):
							trailers = get_trailers(item['movie']['tmdbId'], True)
							if trailers:
								ydl_opts['outtmpl'] = '%s/%s/%s.%s' % (main_folder, foldername, '%(title)s', '%(ext)s')
								with youtube_dl.YoutubeDL(ydl_opts) as ydl:
									ydl.download([trailers[0].geturl()])
					elif item['movie']['hasFile'] == True and has_trailer(foldername):
						info("Deleting %s" % (foldername))
						shutil.rmtree(main_folder+'/'+foldername)

try:
	get_history()
except Exception as e:
	error(e)