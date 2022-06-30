FROM python:3.10.5-alpine
LABEL org.opencontainers.image.source=https://github.com/tomswartz07/pihole-stats-postgres
LABEL org.opencontainers.image.authors="tom+docker@tswartz.net"
LABEL description="Docker container to ingest PiHole data and store it in a PostgreSQL database."

ENV PGHOST="localhost"
ENV PGPORT="5432"
ENV PGDATABASE="pihole"
ENV PGSCHEMA="pihole"
ENV PGUSER="postgres"
# Table for long term stats
ENV PG_PIHOLE_TABLE="piholestats"
# Table for short term data (realtime queries, 10 min interval)
ENV PG_PIHOLE_DISCREET_TABLE="shortdata"
ENV PGPASSWORD=""
ENV PG_SSL_MODE="require"
# Friendly name for host
ENV PIHOLE_INSTANCE_NAME=""
# FQDN of PiHole (must at least have http:// or https://)
ENV PIHOLE_HOST="https://pihole.example.com"
ENV TZ="America/New_York"

RUN apk update && apk add --no-cache postgresql-client
COPY LICENSE .
COPY crontab .
RUN crontab crontab
COPY pihole-api.py .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "crond", "-f" ]
