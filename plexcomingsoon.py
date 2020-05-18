from __future__ import unicode_literals
import requests
import os
import sys
import youtube_dl
import re
import unicodedata
import shutil
from configparser import SafeConfigParser
import time
from logger import debug, info, warning, error, critical, logger
from urllib.parse import urlencode

class PlexComingSoon():
	
	def __init__(self):
		self.parser = SafeConfigParser()
		self.get_config()
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
		self.coming_soon_movies = [str('.placeholder')]
		self.minimumAvailabilityWeigth = ['announced', 'inCinemas', 'released', 'preDB']
	
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
		self.radarr_api_key = self.check_config('radarr_api_key')
		self.trailer_folder = self.check_config('trailer_folder')
		self.interval = int(self.check_config('interval'))
	
	def yt_hook(self, d):
		if d['status'] == 'finished':
			info('File downloaded in %s' % (d['filename']))

	def radarr_request(self, endpoint, params):
		params['apikey'] = self.radarr_api_key
		url = "%s/api/%s?%s" % (self.radarr_url, endpoint, urlencode(params))
		try:
			r = requests.get(url)
			r.raise_for_status()
		except requests.exceptions.Timeout:
			error("Request timeout")
			sys.exit(1)
		except requests.exceptions.TooManyRedirects:
			error("Radarr URL is wrong, check your config")
			sys.exit(1)
		except requests.exceptions.RequestException as e:
			error(str(e))
			sys.exit(1)
		except requests.exceptions.HTTPError as e:
			error(str(e))
			sys.exit(1)
		
		return r.json()
	
	def has_trailer(self, foldername):
		return os.path.exists(self.trailer_folder+'/'+foldername)
	
	def get_history(self):
		params = dict([('page', 1), ('pageSize', 100)])
		response = self.radarr_request('history', params)
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
						self.process(item['movie'])
	
	def get_movies(self):
		response = self.radarr_request('movie', dict([]))
		if 'error' in response:
			raise Exception(response['error'])
		if not response:
			info("No movies found")
		else:
			missing = [x for x in response if self.minimumAvailabilityWeigth.index(x['status']) >= self.minimumAvailabilityWeigth.index(x['minimumAvailability']) and x['monitored'] == True]
			for item in missing:
				self.process(item)

	def process(self, item):
		foldername = "%s (%d)" % (item['title'], item['year'])
		if item['hasFile'] == False:
			self.coming_soon_movies.append(foldername.encode('utf-8'))
			if not self.has_trailer(foldername):
				self.ydl_opts['outtmpl'] = '%s/%s/%s.%s' % (self.trailer_folder, foldername, '%(title)s', '%(ext)s')
				if 'youTubeTrailerId' in item:
					trailer = "https://youtube.com/watch?v=%s" % (item['youTubeTrailerId'])
					with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
						ydl.download([trailer])

	def cleanup(self):
		for x in os.listdir(self.trailer_folder):
			if x not in self.coming_soon_movies:
				path = os.path.join(self.trailer_folder, x)
				info("Deleting %s" % (path))
				shutil.rmtree(path)
		
	def run(self):
		info("Starting search")
		try:
			#self.get_history()
			self.get_movies()
		except Exception as e:
			error(e)
		#self.cleanup()