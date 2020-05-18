FROM alpine:latest

ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

# Update
RUN apk add --update ca-certificates

# Install dependecies
RUN pip install requests youtube-dl schedule

WORKDIR /usr/src/plex-coming-soon
# Create log folder
RUN mkdir logs

COPY logger.py main.py plexcomingsoon.py run.sh ./
RUN chmod 755 run.sh

# map logs to stdout
RUN ln -sf /dev/stdout /usr/src/plex-coming-soon/logs/log.log

VOLUME /trailers

ENV RADARR_URL="" \
    RADARR_API="" \
    INTERVAL="10"

ENTRYPOINT ["./run.sh"]
