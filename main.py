import feedparser
import re
import urllib2
import os
from bs4 import BeautifulSoup
import requests;

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
			print grabbed

try:
	get_history()
except Exception as e:
	print(e);
# def parseRSS(rss_url):
# 	return feedparser.parse(rss_url)

# def purge_dir(dir):
# 	for f in os.listdir(dir):
# 		os.remove(os.path.join(dir, f))

# feed = parseRSS("http://feeds.hd-trailers.net")
# directory = "/mnt/hd/trailers/"
# purge_dir(directory)
# for item in feed['items']:
# 	title = item['title_detail']['value']
# 	title = re.sub("[\(\[].*?[\)\]]", "", title)
# 	title = title.strip()
# 	for content in item['content']:
# 		soup = BeautifulSoup(content['value'], "html.parser")
# 		link = soup.find('a', text='1080p', href=re.compile(".mov$"))
# 		if link:
# 			dl_link = link['href']
# 			filename = title + ".mov"
# 			if not os.path.exists(directory + filename):
# 				u = urllib2.urlopen(dl_link)
# 				f = open(directory + filename, 'wb')
# 				meta = u.info()
# 				file_size = int(meta.getheaders("Content-Length")[0])
# 				print "Downloading %s Bytes: %s" % (filename, file_size)

# 				file_size_dl = 0
# 				block_sz = 8192
# 				while True:
# 					buffer = u.read(block_sz)
# 					if not buffer:
# 						break
# 					file_size_dl += len(buffer)
# 					f.write(buffer)
# 					status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100 / file_size)
# 					status = status + chr(8)*(len(status)+1)
# 					print status,
# 				f.close()
# 			else:
# 				print "%s already exists" % (filename)
		

