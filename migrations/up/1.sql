--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: db_version; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE db_version (
    version integer NOT NULL
);


ALTER TABLE public.db_version OWNER TO postgres;

--
-- Name: db_version_version_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE db_version_version_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.db_version_version_seq OWNER TO postgres;

--
-- Name: db_version_version_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE db_version_version_seq OWNED BY db_version.version;


--
-- Name: layer_feature; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE layer_feature (
    id integer NOT NULL,
    geom geometry(Polygon),
    multi_geom geometry(MultiPolygon),
    "CC_1" character varying(200),
    "CC_2" character varying(200),
    "ENGTYPE4" character varying(200),
    "ENGTYPE_1" character varying(200),
    "ENGTYPE_2" character varying(200),
    "ENGTYPE_3" character varying(200),
    "ENGTYPE_4" character varying(200),
    "ENGTYPE_5" character varying(200),
    "HASC_1" character varying(50),
    "HASC_2" character varying(50),
    "HASC_3" character varying(50),
    "ID_0" character varying(200),
    "ID_1" character varying(200),
    "ID_2" character varying(200),
    "ID_3" character varying(200),
    "ID_4" character varying(200),
    "ID_5" character varying(200),
    "ISO" character varying(200),
    "NAME_0" character varying(200),
    "NAME_1" character varying(200),
    "NAME_2" character varying(200),
    "NAME_3" character varying(200),
    "NAME_4" character varying(200),
    "NAME_5" character varying(200),
    "NL_NAME_1" character varying(200),
    "NL_NAME_2" character varying(200),
    "NL_NAME_3" character varying(200),
    "OBJECTID" character varying(200),
    "REMARKS_1" character varying(200),
    "REMARKS_2" character varying(200),
    "REMARKS_3" character varying(200),
    "REMARKS_4" character varying(200),
    "Shape_Area" character varying(200),
    "Shape_Leng" character varying(200),
    "TYPE4" character varying(200),
    "TYPE_1" character varying(200),
    "TYPE_2" character varying(200),
    "TYPE_3" character varying(200),
    "TYPE_4" character varying(200),
    "TYPE_5" character varying(200),
    "VALIDFR_1" character varying(200),
    "VALIDFR_2" character varying(200),
    "VALIDFR_3" character varying(200),
    "VALIDFR_4" character varying(200),
    "VALIDTO_1" character varying(200),
    "VALIDTO_2" character varying(200),
    "VALIDTO_3" character varying(200),
    "VALIDTO_4" character varying(200),
    "VARNAME_1" character varying(200),
    "VARNAME_2" character varying(200),
    "VARNAME_3" character varying(200),
    "VARNAME_4" character varying(200)
);


ALTER TABLE public.layer_feature OWNER TO postgres;

--
-- Name: layer_feature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE layer_feature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.layer_feature_id_seq OWNER TO postgres;

--
-- Name: layer_feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE layer_feature_id_seq OWNED BY layer_feature.id;


--
-- Name: version; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY db_version ALTER COLUMN version SET DEFAULT nextval('db_version_version_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY layer_feature ALTER COLUMN id SET DEFAULT nextval('layer_feature_id_seq'::regclass);


--
-- Name: db_version_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY db_version
    ADD CONSTRAINT db_version_pkey PRIMARY KEY (version);


--
-- Name: layer_feature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY layer_feature
    ADD CONSTRAINT layer_feature_pkey PRIMARY KEY (id);


--
-- Name: idx_layer_feature_geom; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE INDEX idx_layer_feature_geom ON layer_feature USING gist (geom);


--
-- Name: idx_layer_feature_multi_geom; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE INDEX idx_layer_feature_multi_geom ON layer_feature USING gist (multi_geom);


/* Note: Commented out due to postgres bugs */
/* http://www.postgresql.org/message-id/20121211144710.GC5062@alap2.lan */
/* -- */
/* -- Name: geometry_columns_delete; Type: RULE; Schema: public; Owner: postgres */
/* -- */

/* CREATE RULE geometry_columns_delete AS ON DELETE TO geometry_columns DO INSTEAD NOTHING; */


/* -- */
/* -- Name: geometry_columns_insert; Type: RULE; Schema: public; Owner: postgres */
/* -- */

/* CREATE RULE geometry_columns_insert AS ON INSERT TO geometry_columns DO INSTEAD NOTHING; */


/* -- */
/* -- Name: geometry_columns_update; Type: RULE; Schema: public; Owner: postgres */
/* -- */

/* CREATE RULE geometry_columns_update AS ON UPDATE TO geometry_columns DO INSTEAD NOTHING; */



--
-- PostgreSQL database dump complete
--



INSERT INTO db_version (version) VALUES ('1');
