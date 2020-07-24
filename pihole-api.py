#!/usr/bin/env python
"""
Grab stats from PiHole and put em someplace else
"""

import json
from contextlib import closing
import datetime
import socket
from requests import get
from requests.exceptions import RequestException
import psycopg2

# Database params
dbname = "pihole"
dbschema = "pihole"
statstable = "piholestats"
discretetable = "shortdata"
dbhost = ""
dbport = ""
dbuser = ""
dbpassword = ""
dbappname = "PiHole Stats Aggregator"
piholehost = "https://hostname.net" # Do not add the API path, just the address of PiHole
hostname = socket.gethostname()

def connect_to_db(db, user, host, password, port, appname, schema):
    "Handle connecting to db"
    connection = "dbname='%s' user='%s' host='%s' password='%s' port='%s' application_name='%s' options='-csearch_path=%s'" % (
        db, user, host, password, port, appname, schema
        )
    try:
        return psycopg2.connect(connection)
    except psycopg2.Error as e:
        print("Error connecting to db")
        print(e.pgcode)
        print(e.pgerror)
        return None

def commit_sql(conn, sql_statement):
    "Handles committing queries to the db, single transactions"
    try:
        cur = conn.cursor()
        cur.execute(sql_statement)
        conn.commit()
        cur.close()
        return ['ok', 'success', 'OK']
    except Exception as e:
        print("Issue detected: ", e)
        return ['remove', 'danger', 'Issue Detected']

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            print("Unable to get page...")
            raise RequestException
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            #and content_type is not None)
            and content_type.find('application/json') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

#  "gravity_last_updated": {
#    "file_exists": true,
#    "absolute": 1588491735,
#    "relative": {
#      "days": "0",
#      "hours": "14",
#      "minutes": "42"
#    }

raw_data = simple_get(piholehost + '/admin/api.php')
if raw_data is not None:
    parsed_json = json.loads(raw_data)
else:
    pass

discrete_data = simple_get(piholehost + '/admin/api.php?overTimeData10mins')
if discrete_data is not None:
    short_json = json.loads(discrete_data)
    domains = short_json['domains_over_time']
    ads = short_json['ads_over_time']
    for time in domains:
        insert_statement2 = "INSERT INTO {}.{} ".format(dbschema, discretetable)
        insert_statement2 += "(domains,"
        insert_statement2 += " hostname,"
        insert_statement2 += " epoch) "
        insert_statement2 += "VALUES"
        insert_statement2 += " ('" + str(domains[time]) + "',"
        insert_statement2 += " '" + hostname + "',"
        insert_statement2 += " to_timestamp('" + time + "'))"
        insert_statement2 += " ON CONFLICT (epoch) DO"
        insert_statement2 += " UPDATE SET"
        insert_statement2 += " domains ="
        insert_statement2 += " EXCLUDED.domains;"
        client = connect_to_db(dbname, dbuser, dbhost, dbpassword, dbport, dbappname, dbschema)
        commit_sql(client, insert_statement2)
    for time in ads:
        insert_statement3 = "INSERT INTO {}.{} ".format(dbschema, discretetable)
        insert_statement3 += "(ads,"
        insert_statement3 += " hostname,"
        insert_statement3 += " epoch) "
        insert_statement3 += "VALUES"
        insert_statement3 += " ('" + str(ads[time]) + "',"
        insert_statement3 += " '" + hostname + "',"
        insert_statement3 += " to_timestamp('" + time + "'))"
        insert_statement3 += " ON CONFLICT (epoch) DO"
        insert_statement3 += " UPDATE SET"
        insert_statement3 += " ads ="
        insert_statement3 += " EXCLUDED.ads;"
        client = connect_to_db(dbname, dbuser, dbhost, dbpassword, dbport, dbappname, dbschema)
        commit_sql(client, insert_statement3)
else:
    pass

domains_being_blocked = str(parsed_json['domains_being_blocked'])
dns_queries_today = str(parsed_json['dns_queries_today'])
ads_blocked_today = str(parsed_json['ads_blocked_today'])
ads_percentage_today = str(parsed_json['ads_percentage_today'])
unique_domains = str(parsed_json['unique_domains'])
domains_forwarded = str(parsed_json['queries_forwarded'])
queries_cached = str(parsed_json['queries_cached'])
clients_ever_seen = str(parsed_json['clients_ever_seen'])
unique_clients = str(parsed_json['unique_clients'])
dns_queries_all_types = str(parsed_json['dns_queries_all_types'])
reply_NODATA = str(parsed_json['reply_NODATA'])
reply_NXDOMAIN = str(parsed_json['reply_NXDOMAIN'])
reply_CNAME = str(parsed_json['reply_CNAME'])
reply_IP = str(parsed_json['reply_IP'])
privacy_level = str(parsed_json['privacy_level'])
status_level = str(parsed_json['status'])
gravity_last_updated = str(parsed_json['gravity_last_updated']['absolute'])

insert_statement = "INSERT INTO {}.{} ".format(dbschema, statstable)
insert_statement += " (domains_being_blocked,"
insert_statement += " dns_queries_today,"
insert_statement += " ads_blocked_today,"
insert_statement += " ads_percentage_today,"
insert_statement += " unique_domains,"
insert_statement += " domains_forwarded,"
insert_statement += " queries_cached,"
insert_statement += " clients_ever_seen,"
insert_statement += " unique_clients,"
insert_statement += " dns_queries_all_types,"
insert_statement += " reply_NODATA,"
insert_statement += " reply_NXDOMAIN,"
insert_statement += " reply_CNAME,"
insert_statement += " reply_IP,"
insert_statement += " privacy_level,"
insert_statement += " status_level,"
insert_statement += " time,"
insert_statement += " hostname,"
insert_statement += " gravity_last_updated)"
insert_statement += "VALUES"
insert_statement += " ('" + domains_being_blocked + "',"
insert_statement += " '" + dns_queries_today + "',"
insert_statement += " '" + ads_blocked_today + "',"
insert_statement += " '" + ads_percentage_today + "',"
insert_statement += " '" + unique_domains + "',"
insert_statement += " '" + domains_forwarded + "',"
insert_statement += " '" + queries_cached + "',"
insert_statement += " '" + clients_ever_seen + "',"
insert_statement += " '" + unique_clients + "',"
insert_statement += " '" + dns_queries_all_types + "',"
insert_statement += " '" + reply_NODATA + "',"
insert_statement += " '" + reply_NXDOMAIN + "',"
insert_statement += " '" + reply_CNAME + "',"
insert_statement += " '" + reply_IP + "',"
insert_statement += " '" + privacy_level + "',"
insert_statement += " '" + status_level + "',"
insert_statement += " '" + str(datetime.datetime.now()) + "',"
insert_statement += " '" + hostname + "',"
insert_statement += " to_timestamp('" + gravity_last_updated + "'))"
insert_statement += " ON CONFLICT DO NOTHING;"

client = connect_to_db(dbname, dbuser, dbhost, dbpassword, dbport, dbappname, dbschema)
commit_sql(client, insert_statement)
