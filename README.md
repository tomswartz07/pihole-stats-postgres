# PiHole PostgreSQL Exporter

Export your PiHole stats to Postgres for better, longer retention of your data.


## Using

To use this script, simply run it:
```
python pihole-api.py
```

It's recommended that a virtualenv is used, for sanity reasons:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python pihole-api.py
```

This script is intended to be run regularly and frequently so that it could
capture long-term PiHole statistics.
Consider scripting this to run as a cron job.


This is a very hacky script, done quickly as a proof-of-concept.
Pull requests welcome.
