### Description ###
The script calls radarr api to get the last 100 movies grabbed and not downloaded yet and downloads its trailer to the specified folder. It will also delete trailers of movie successfully downloaded.
You have to create a new library in Plex (for example a "Coming soon" library) and point it to trailers folder.
Your users will be able to watch the trailer of the movies that will be shortly available on your plex server.

### Usage ###
~~~
docker create \
--name plexcomingsoon \
-e RADARR_URL="<radarr url>" \
-e TMDB_API="<tmdb api key>" \
-e RADARR_API="<radarr api key>" \
-e LANG="<language tag>" \
-e COUNTRY="<country tag>" \
-e INTERVAL="<interval>" \
-v <path/to/trailers/folder>:/trailers \
andyts93/plex-coming-soon
~~~


### Parameters ###
* `-e RADARR_URL` - URL of your radarr installation (default http://localhost:7878)
* `-e TMDB_API` - Your TMDB API key, to get one you have to register to [TheMovieDB](http://themoviedb.org) and read the [api key faq](https://www.themoviedb.org/faq/api)
* `-e RADARR_API` - Your radarr api key, you can obtain it going into radarr settings => general
* `-e INTERVAL` - Interval in minutes (i.e. with a value of 10 the script will check and download trailers every 10 minutes)
