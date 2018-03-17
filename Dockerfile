FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install dependecies
RUN pip install requests youtube-dl schedule

WORKDIR /usr/src/plex-coming-soon
RUN mkdir logs

COPY config.sample.ini ./lib logger.py main.py plexcomingsoon.py run.sh ./

VOLUME /trailers

ENV TMDB_API=""
