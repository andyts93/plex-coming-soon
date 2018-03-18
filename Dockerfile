FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install dependecies
RUN pip install requests youtube-dl schedule

WORKDIR /usr/src/plex-coming-soon
RUN mkdir logs

COPY ./lib logger.py main.py plexcomingsoon.py run.sh ./
RUN chmod 755 run.sh

VOLUME /trailers

ENV RADARR_URL="" \
    TMDB_API="" \
    RADARR_API="" \
    LANG="en" \
    COUNTRY="gb" \
    INTERVAL="10"

ENTRYPOINT ["./run.sh"]
