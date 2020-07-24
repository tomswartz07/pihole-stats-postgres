--
-- PostgreSQL database dump
--


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: coronavirus; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE pihole WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE pihole OWNER TO postgres;

\connect pihole

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: covid19; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA pihole;

ALTER SCHEMA pihole OWNER TO postgres;

SET default_tablespace = '';

CREATE SEQUENCE pihole.id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE pihole.id_seq OWNER TO postgres;

--
-- Name: shortdata; Type: TABLE; Schema: pihole; Owner: -
--

CREATE TABLE pihole.shortdata (
    epoch timestamp without time zone NOT NULL,
    domains integer,
    ads integer,
    hostname text
);

--
-- Name: shortdata shortdata_pkey; Type: CONSTRAINT; Schema: pihole; Owner: -
--

ALTER TABLE ONLY pihole.shortdata
    ADD CONSTRAINT shortdata_pkey PRIMARY KEY (epoch);

--
-- Name: piholestats; Type: TABLE; Schema: pihole; Owner: -
--

CREATE TABLE pihole.piholestats (
    id bigint DEFAULT nextval('pihole.id_seq'::regclass) NOT NULL,
    "time" timestamp with time zone NOT NULL,
    domains_being_blocked integer NOT NULL,
    dns_queries_today integer NOT NULL,
    ads_blocked_today integer NOT NULL,
    ads_percentage_today real NOT NULL,
    unique_domains integer NOT NULL,
    domains_forwarded integer NOT NULL,
    queries_cached integer NOT NULL,
    clients_ever_seen integer NOT NULL,
    unique_clients integer NOT NULL,
    dns_queries_all_types integer NOT NULL,
    reply_nodata integer NOT NULL,
    reply_nxdomain integer NOT NULL,
    reply_cname integer NOT NULL,
    reply_ip integer NOT NULL,
    privacy_level integer,
    status_level text,
    gravity_last_updated timestamp without time zone,
    hostname text
);

--
-- Name: piholestats pihole_stats_pkey; Type: CONSTRAINT; Schema: pihole; Owner: -
--

ALTER TABLE ONLY pihole.piholestats
    ADD CONSTRAINT pihole_stats_pkey PRIMARY KEY (id);

--
-- Name: piholestats unique_time; Type: CONSTRAINT; Schema: pihole; Owner: -
--

ALTER TABLE ONLY pihole.piholestats
    ADD CONSTRAINT unique_time UNIQUE ("time");

--
-- Name: idx_hostname; Type: INDEX; Schema: pihole; Owner: -
--

CREATE INDEX idx_hostname ON pihole.piholestats USING btree (hostname);

--
-- Name: idx_time; Type: INDEX; Schema: pihole; Owner: -
--

CREATE INDEX idx_time ON pihole.piholestats USING btree ("time") INCLUDE ("time");

GRANT ALL ON SCHEMA pihole TO postgres;
GRANT USAGE ON SCHEMA pihole TO grafana;

GRANT ALL ON TABLE pihole.piholestats TO postgres;
GRANT SELECT ON TABLE pihole.piholestats TO grafana;
GRANT SELECT ON TABLE pihole.shortdata TO grafana;

--
-- PostgreSQL database dump complete
--

