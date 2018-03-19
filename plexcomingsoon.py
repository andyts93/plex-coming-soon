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

class PlexComingSoon():
	
	def __init__(self):
		self.parser = SafeConfigParser()
		self.get_config()
		# set tmdb info
		set_locale(self.language, self.country)
		set_key(self.tmdb_api_key)
		# youtube-dl options
		self.ydl_opts = {
			'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
			'ignoreerrors': True,
			'no_warnings': True,
			'logger': logger,
			'verbose': False,
			'progress_hooks': [self.yt_hook],
			# "simulate": True
		}
	
	def check_config(self, option):
		try:
			value = self.parser.get('DEFAULT', option)
			if value:
				return value
			else:
				error("%s option missing" % (option))
				exit()
		except Exception as e:
			error(str(e))
			exit()

	def get_config(self):
		# get config file
		settings_file = os.path.abspath(os.path.dirname(__file__))+'/config.ini'
		found = self.parser.read(settings_file)
		if not found:
			critical("Configuration file not found, check your config.ini file")
			exit()
		
		# get configs
		self.radarr_url = self.check_config('radarr_url')
		self.tmdb_api_key = self.check_config('tmdb_api_key')
		self.radarr_api_key = self.check_config('radarr_api_key')
		self.language = self.check_config('language')
		self.country = self.check_config('country')
		self.trailer_folder = self.check_config('trailer_folder')
		self.interval = int(self.check_config('interval'))
	
	def yt_hook(self, d):
		if d['status'] == 'finished':
			info('File downloaded in %s' % (d['filename']))
	
	def get_trailers(self, tmdbId, retry):
		try:
			debug("Searching for movie with id %d" % (tmdbId))
			movie = Movie(tmdbId)
			if movie:
				trailers = movie.youtube_trailers
				if not trailers and retry == True:
					# try to get english trailer
					debug("Trying to get english trailer")
					set_locale('en', 'gb')
					return self.get_trailers(tmdbId, False)
				else:
					set_locale(self.language, self.country)
					return trailers
			else:
				error("No movie found with id %d" % (tmdbId))
		except Exception as e:
			if str(e) == '25':
				info("API limit reached, sleep for 10 seconds")
				time.sleep(10)
				return self.get_trailers(tmdbId, retry)
	
	def has_trailer(self, foldername):
		return os.path.exists(self.trailer_folder+'/'+foldername)
	
	def get_history(self):
		url = "%s/api/history?page=1&pageSize=100&apikey=%s" % (self.radarr_url, self.radarr_api_key)
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
							if not self.has_trailer(foldername):
								trailers = self.get_trailers(item['movie']['tmdbId'], True)
								if trailers:
									self.ydl_opts['outtmpl'] = '%s/%s/%s.%s' % (self.trailer_folder, foldername, '%(title)s', '%(ext)s')
									with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
										ydl.download([trailers[0].geturl()])
						elif item['movie']['hasFile'] == True and self.has_trailer(foldername):
							info("Deleting %s" % (foldername))
							shutil.rmtree(self.trailer_folder+'/'+foldername)
		
	def run(self):
		info("Starting search")
		try:
			self.get_history()
		except Exception as e:
			error(e)