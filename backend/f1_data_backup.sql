--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

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

ALTER TABLE ONLY public.sprint_results DROP CONSTRAINT sprint_results_race_id_fkey;
ALTER TABLE ONLY public.sprint_results DROP CONSTRAINT sprint_results_driver_id_fkey;
ALTER TABLE ONLY public.sprint_results DROP CONSTRAINT sprint_results_constructor_id_fkey;
ALTER TABLE ONLY public.results DROP CONSTRAINT results_race_id_fkey;
ALTER TABLE ONLY public.results DROP CONSTRAINT results_driver_id_fkey;
ALTER TABLE ONLY public.results DROP CONSTRAINT results_constructor_id_fkey;
ALTER TABLE ONLY public.races DROP CONSTRAINT races_season_id_fkey;
ALTER TABLE ONLY public.races DROP CONSTRAINT races_circuit_id_fkey;
ALTER TABLE ONLY public.qualifying_results DROP CONSTRAINT qualifying_results_race_id_fkey;
ALTER TABLE ONLY public.qualifying_results DROP CONSTRAINT qualifying_results_driver_id_fkey;
ALTER TABLE ONLY public.qualifying_results DROP CONSTRAINT qualifying_results_constructor_id_fkey;
ALTER TABLE ONLY public.driver_standings DROP CONSTRAINT driver_standings_season_id_fkey;
ALTER TABLE ONLY public.driver_standings DROP CONSTRAINT driver_standings_driver_id_fkey;
ALTER TABLE ONLY public.driver_standings DROP CONSTRAINT driver_standings_constructor_id_fkey;
ALTER TABLE ONLY public.driver_seasons DROP CONSTRAINT driver_seasons_season_id_fkey;
ALTER TABLE ONLY public.driver_seasons DROP CONSTRAINT driver_seasons_driver_id_fkey;
ALTER TABLE ONLY public.driver_seasons DROP CONSTRAINT driver_seasons_constructor_id_fkey;
ALTER TABLE ONLY public.constructors DROP CONSTRAINT constructors_season_id_fkey;
ALTER TABLE ONLY public.constructor_standings DROP CONSTRAINT constructor_standings_season_id_fkey;
ALTER TABLE ONLY public.constructor_standings DROP CONSTRAINT constructor_standings_constructor_id_fkey;
DROP INDEX public.ix_sprint_results_id;
DROP INDEX public.ix_seasons_year;
DROP INDEX public.ix_seasons_id;
DROP INDEX public.ix_results_id;
DROP INDEX public.ix_races_id;
DROP INDEX public.ix_qualifying_results_id;
DROP INDEX public.ix_drivers_driver_id;
DROP INDEX public.ix_driver_standings_id;
DROP INDEX public.ix_driver_seasons_id;
DROP INDEX public.ix_constructors_constructor_id;
DROP INDEX public.ix_constructor_standings_id;
DROP INDEX public.ix_circuits_circuit_id;
DROP INDEX public.idx_driver_standing_season_driver;
DROP INDEX public.idx_driver_standing_season_constructor;
DROP INDEX public.idx_driver_standing_season;
DROP INDEX public.idx_constructor_standing_season_constructor;
DROP INDEX public.idx_constructor_standing_season;
ALTER TABLE ONLY public.sprint_results DROP CONSTRAINT sprint_results_pkey;
ALTER TABLE ONLY public.seasons DROP CONSTRAINT seasons_pkey;
ALTER TABLE ONLY public.results DROP CONSTRAINT results_pkey;
ALTER TABLE ONLY public.races DROP CONSTRAINT races_pkey;
ALTER TABLE ONLY public.qualifying_results DROP CONSTRAINT qualifying_results_pkey;
ALTER TABLE ONLY public.drivers DROP CONSTRAINT drivers_pkey;
ALTER TABLE ONLY public.driver_standings DROP CONSTRAINT driver_standings_pkey;
ALTER TABLE ONLY public.driver_seasons DROP CONSTRAINT driver_seasons_pkey;
ALTER TABLE ONLY public.constructors DROP CONSTRAINT constructors_pkey;
ALTER TABLE ONLY public.constructor_standings DROP CONSTRAINT constructor_standings_pkey;
ALTER TABLE ONLY public.circuits DROP CONSTRAINT circuits_pkey;
ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
ALTER TABLE public.sprint_results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.seasons ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.races ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.qualifying_results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.driver_standings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.driver_seasons ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.constructor_standings ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.sprint_results_id_seq;
DROP TABLE public.sprint_results;
DROP SEQUENCE public.seasons_id_seq;
DROP TABLE public.seasons;
DROP SEQUENCE public.results_id_seq;
DROP TABLE public.results;
DROP SEQUENCE public.races_id_seq;
DROP TABLE public.races;
DROP SEQUENCE public.qualifying_results_id_seq;
DROP TABLE public.qualifying_results;
DROP TABLE public.drivers;
DROP SEQUENCE public.driver_standings_id_seq;
DROP TABLE public.driver_standings;
DROP SEQUENCE public.driver_seasons_id_seq;
DROP TABLE public.driver_seasons;
DROP TABLE public.constructors;
DROP SEQUENCE public.constructor_standings_id_seq;
DROP TABLE public.constructor_standings;
DROP TABLE public.circuits;
DROP TABLE public.alembic_version;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: circuits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.circuits (
    circuit_id character varying(50) NOT NULL,
    circuit_url character varying(500),
    circuit_name character varying(200) NOT NULL,
    lat double precision,
    long double precision,
    locality character varying(100),
    country character varying(100),
    length double precision,
    corners integer,
    lap_record character varying(50),
    lap_record_driver character varying(100),
    lap_record_year integer,
    description text,
    characteristics text,
    is_active boolean NOT NULL,
    first_grand_prix integer,
    typical_lap_count integer,
    race_distance double precision,
    circuit_layout_image_url character varying(500),
    circuit_layout_image_path character varying(500)
);


--
-- Name: constructor_standings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.constructor_standings (
    id integer NOT NULL,
    season_id integer NOT NULL,
    constructor_id character varying(50) NOT NULL,
    "position" integer,
    points double precision NOT NULL,
    wins integer NOT NULL,
    position_text character varying(10)
);


--
-- Name: constructor_standings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.constructor_standings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: constructor_standings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.constructor_standings_id_seq OWNED BY public.constructor_standings.id;


--
-- Name: constructors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.constructors (
    constructor_id character varying(50) NOT NULL,
    constructor_url character varying(500),
    constructor_name character varying(200) NOT NULL,
    constructor_nationality character varying(100),
    season_id integer NOT NULL,
    base character varying(200),
    team_chief character varying(100),
    technical_chief character varying(100),
    power_unit character varying(100),
    is_active boolean NOT NULL,
    championships integer NOT NULL,
    wins integer NOT NULL,
    podiums integer NOT NULL,
    poles integer NOT NULL,
    fastest_laps integer NOT NULL
);


--
-- Name: driver_seasons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_seasons (
    id integer NOT NULL,
    driver_id character varying(50) NOT NULL,
    constructor_id character varying(50) NOT NULL,
    season_id integer NOT NULL
);


--
-- Name: driver_seasons_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.driver_seasons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: driver_seasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.driver_seasons_id_seq OWNED BY public.driver_seasons.id;


--
-- Name: driver_standings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_standings (
    id integer NOT NULL,
    season_id integer NOT NULL,
    driver_id character varying(50) NOT NULL,
    constructor_id character varying(50) NOT NULL,
    "position" integer,
    points double precision NOT NULL,
    wins integer NOT NULL,
    position_text character varying(10)
);


--
-- Name: driver_standings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.driver_standings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: driver_standings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.driver_standings_id_seq OWNED BY public.driver_standings.id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.drivers (
    driver_id character varying(50) NOT NULL,
    driver_number integer,
    driver_code character varying(10),
    driver_url character varying(500),
    given_name character varying(100) NOT NULL,
    family_name character varying(100) NOT NULL,
    date_of_birth date,
    driver_nationality character varying(100)
);


--
-- Name: qualifying_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.qualifying_results (
    id integer NOT NULL,
    race_id integer NOT NULL,
    driver_id character varying(50) NOT NULL,
    constructor_id character varying(50) NOT NULL,
    number integer,
    "position" integer,
    q1_time character varying(100),
    q2_time character varying(100),
    q3_time character varying(100)
);


--
-- Name: qualifying_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.qualifying_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: qualifying_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.qualifying_results_id_seq OWNED BY public.qualifying_results.id;


--
-- Name: races; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.races (
    id integer NOT NULL,
    season_id integer NOT NULL,
    circuit_id character varying(50) NOT NULL,
    round_number integer NOT NULL,
    country character varying(100),
    location character varying(100),
    official_event_name character varying(200) NOT NULL,
    event_date date,
    event_format character varying(50),
    session1 character varying(100),
    session1_date timestamp without time zone,
    session2 character varying(100),
    session2_date timestamp without time zone,
    session3 character varying(100),
    session3_date timestamp without time zone,
    session4 character varying(100),
    session4_date timestamp without time zone,
    session5 character varying(100),
    session5_date timestamp without time zone,
    is_sprint boolean NOT NULL
);


--
-- Name: races_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.races_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: races_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.races_id_seq OWNED BY public.races.id;


--
-- Name: results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.results (
    id integer NOT NULL,
    race_id integer NOT NULL,
    driver_id character varying(50) NOT NULL,
    constructor_id character varying(50) NOT NULL,
    number integer,
    "position" integer,
    position_text character varying(10),
    points double precision,
    grid integer,
    laps integer,
    status character varying(50),
    total_race_time_millis bigint,
    total_race_time character varying(100),
    fastest_lap_rank integer,
    fastest_lap_number integer,
    fastest_lap_time character varying(100)
);


--
-- Name: results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.results_id_seq OWNED BY public.results.id;


--
-- Name: seasons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.seasons (
    id integer NOT NULL,
    year integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying,
    start_date date,
    end_date date
);


--
-- Name: seasons_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.seasons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: seasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.seasons_id_seq OWNED BY public.seasons.id;


--
-- Name: sprint_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sprint_results (
    id integer NOT NULL,
    race_id integer NOT NULL,
    driver_id character varying(50) NOT NULL,
    constructor_id character varying(50) NOT NULL,
    number integer,
    "position" integer,
    position_text character varying(10),
    points double precision NOT NULL,
    grid integer,
    status character varying(50),
    laps integer,
    fastest_lap_time character varying(100),
    fastest_lap_rank integer,
    fastest_lap_number integer,
    total_race_time character varying(100),
    total_race_time_millis integer
);


--
-- Name: sprint_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sprint_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sprint_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sprint_results_id_seq OWNED BY public.sprint_results.id;


--
-- Name: constructor_standings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructor_standings ALTER COLUMN id SET DEFAULT nextval('public.constructor_standings_id_seq'::regclass);


--
-- Name: driver_seasons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_seasons ALTER COLUMN id SET DEFAULT nextval('public.driver_seasons_id_seq'::regclass);


--
-- Name: driver_standings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_standings ALTER COLUMN id SET DEFAULT nextval('public.driver_standings_id_seq'::regclass);


--
-- Name: qualifying_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualifying_results ALTER COLUMN id SET DEFAULT nextval('public.qualifying_results_id_seq'::regclass);


--
-- Name: races id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.races ALTER COLUMN id SET DEFAULT nextval('public.races_id_seq'::regclass);


--
-- Name: results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results ALTER COLUMN id SET DEFAULT nextval('public.results_id_seq'::regclass);


--
-- Name: seasons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seasons ALTER COLUMN id SET DEFAULT nextval('public.seasons_id_seq'::regclass);


--
-- Name: sprint_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sprint_results ALTER COLUMN id SET DEFAULT nextval('public.sprint_results_id_seq'::regclass);


--
-- Data for Name: circuits; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.circuits (circuit_id, circuit_url, circuit_name, lat, long, locality, country, length, corners, lap_record, lap_record_driver, lap_record_year, description, characteristics, is_active, first_grand_prix, typical_lap_count, race_distance, circuit_layout_image_url, circuit_layout_image_path) FROM stdin;
hungaroring	https://en.wikipedia.org/wiki/Hungaroring	Hungaroring	47.5789	19.2486	Budapest	Hungary	4381	\N	1:16.627	Lewis Hamilton	2020	\N	\N	t	1986	70	306.63	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.webp	static/circuit_images/hungaroring_circuit.webp
red_bull_ring	https://en.wikipedia.org/wiki/Red_Bull_Ring	Red Bull Ring	47.2197	14.7647	Spielberg	Austria	4326	\N	1:07.924	Oscar Piastri	2025	\N	\N	t	1970	71	307.018	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.webp	static/circuit_images/red_bull_ring_circuit.webp
rodriguez	https://en.wikipedia.org/wiki/Aut%C3%B3dromo_Hermanos_Rodr%C3%ADguez	Autódromo Hermanos Rodríguez	19.4042	-99.0907	Mexico City	Mexico	4304	\N	1:17.774	Valtteri Bottas	2021	\N	\N	t	1963	71	305.354	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.webp	static/circuit_images/rodriguez_circuit.webp
yas_marina	https://en.wikipedia.org/wiki/Yas_Marina_Circuit	Yas Marina Circuit	24.4672	54.6031	Abu Dhabi	UAE	5281	\N	1:25.637	Kevin Magnussen	2024	\N	\N	f	2009	58	306.183	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.webp	static/circuit_images/yas_marina_circuit.webp
shanghai	https://en.wikipedia.org/wiki/Shanghai_International_Circuit	Shanghai International Circuit	31.3389	121.22	Shanghai	China	5451	\N	1:32.238	Michael Schumacher	2004	\N	\N	t	2004	56	305.066	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.webp	static/circuit_images/shanghai_circuit.webp
suzuka	https://en.wikipedia.org/wiki/Suzuka_International_Racing_Course	Suzuka Circuit	34.8431	136.541	Suzuka	Japan	5807	\N	1:30.965	Kimi Antonelli	2025	\N	\N	t	1987	53	307.471	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.webp	static/circuit_images/suzuka_circuit.webp
zandvoort	https://en.wikipedia.org/wiki/Circuit_Zandvoort	Circuit Park Zandvoort	52.3888	4.54092	Zandvoort	Netherlands	4259	\N	1:11.097	Lewis Hamilton	2021	\N	\N	t	1952	72	306.587	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.webp	static/circuit_images/zandvoort_circuit.webp
baku	https://en.wikipedia.org/wiki/Baku_City_Circuit	Baku City Circuit	40.3725	49.8533	Baku	Azerbaijan	6003	\N	1:43.009	Charles Leclerc	2019	\N	\N	t	2016	51	306.049	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.webp	static/circuit_images/Baku_Circuit.webp
catalunya	https://en.wikipedia.org/wiki/Circuit_de_Barcelona-Catalunya	Circuit de Barcelona-Catalunya	41.57	2.26111	Montmeló	Spain	4657	\N	1:15.743	Oscar Piastri	2025	\N	\N	f	1991	66	307.236	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.webp	static/circuit_images/catalunya_circuit.webp
monaco	https://en.wikipedia.org/wiki/Circuit_de_Monaco	Circuit de Monaco	43.7347	7.42056	Monte-Carlo	Monaco	3337	\N	1:12.909	Lewis Hamilton	2021	\N	\N	f	1950	78	260.286	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.webp	static/circuit_images/monaco_circuit.webp
vegas	https://en.wikipedia.org/wiki/Las_Vegas_Grand_Prix#Circuit	Las Vegas Strip Street Circuit	36.1147	-115.173	Las Vegas	USA	6201	\N	1:34.876	Lando Norris	2024	\N	\N	f	2023	50	309.958	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.webp	static/circuit_images/vegas_circuit.webp
albert_park	https://en.wikipedia.org/wiki/Albert_Park_Circuit	Albert Park Grand Prix Circuit	-37.8497	144.968	Melbourne	Australia	5278	\N	1:19.813	Charles Leclerc	2024	\N	\N	t	1996	58	306.124	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.webp	static/circuit_images/albert_park_circuit.webp
bahrain	https://en.wikipedia.org/wiki/Bahrain_International_Circuit	Bahrain International Circuit	26.0325	50.5106	Sakhir	Bahrain	5412	\N	1:31.447	Pedro de la Rosa	2005	\N	\N	t	2004	57	308.238	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.webp	static/circuit_images/bahrain_circuit.webp
interlagos	https://en.wikipedia.org/wiki/Interlagos_Circuit	Autódromo José Carlos Pace	-23.7036	-46.6997	São Paulo	Brazil	4309	\N	1:10.540	Valtteri Bottas	2018	\N	\N	t	1973	71	305.879	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.webp	static/circuit_images/interlagos_circuit.webp
jeddah	https://en.wikipedia.org/wiki/Jeddah_Corniche_Circuit	Jeddah Corniche Circuit	21.6319	39.1044	Jeddah	Saudi Arabia	6174	\N	1:30.734	Lewis Hamilton	2021	\N	\N	t	2021	50	308.45	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.webp	static/circuit_images/jeddah_circuit.webp
marina_bay	https://en.wikipedia.org/wiki/Marina_Bay_Street_Circuit	Marina Bay Street Circuit	1.2914	103.864	Marina Bay	Singapore	4940	\N	1:34.486	Daniel Ricciardo	2024	\N	\N	t	2008	62	306.143	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.webp	static/circuit_images/marina_bay_circuit.webp
monza	https://en.wikipedia.org/wiki/Monza_Circuit	Autodromo Nazionale di Monza	45.6156	9.28111	Monza	Italy	5793	\N	1:21.046	Rubens Barrichello	2004	\N	\N	t	1950	53	306.72	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.webp	static/circuit_images/monza_circuit.webp
spa	https://en.wikipedia.org/wiki/Circuit_de_Spa-Francorchamps	Circuit de Spa-Francorchamps	50.4372	5.97139	Spa	Belgium	7004	\N	1:44.701	Sergio Perez	2024	\N	\N	f	1950	44	308.052	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.webp	static/circuit_images/spa_circuit.webp
losail	https://en.wikipedia.org/wiki/Lusail_International_Circuit	Losail International Circuit	25.49	51.4542	Al Daayen	Qatar	5419	\N	1:22.384	Lando Norris	2024	\N	\N	f	2021	57	308.611	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Qatar_Circuit.webp	static/circuit_images/losail_circuit.webp
miami	https://en.wikipedia.org/wiki/Miami_International_Autodrome	Miami International Autodrome	25.9581	-80.2389	Miami	USA	5412	\N	1:29.708	Max Verstappen	2023	\N	\N	f	2022	57	308.326	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.webp	static/circuit_images/miami_circuit.webp
silverstone	https://en.wikipedia.org/wiki/Silverstone_Circuit	Silverstone Circuit	52.0786	-1.01694	Silverstone	UK	5891	\N	1:27.097	Max Verstappen	2020	\N	\N	f	1950	52	306.198	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.webp	static/circuit_images/silverstone_circuit.webp
villeneuve	https://en.wikipedia.org/wiki/Circuit_Gilles_Villeneuve	Circuit Gilles Villeneuve	45.5	-73.5228	Montreal	Canada	4361	\N	1:13.078	Valtteri Bottas	2019	\N	\N	f	1978	70	305.27	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.webp	static/circuit_images/villeneuve_circuit.webp
imola	https://en.wikipedia.org/wiki/Imola_Circuit	Autodromo Enzo e Dino Ferrari	44.3439	11.7167	Imola	Italy	4909	\N	1:15.484	Lewis Hamilton	2020	\N	\N	t	1980	63	309.049	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Emilia_Romagna_Circuit.webp	static/circuit_images/imola_circuit.webp
americas	https://en.wikipedia.org/wiki/Circuit_of_the_Americas	Circuit of the Americas	30.1328	-97.6411	Austin	USA	5513	\N	1:36.169	Charles Leclerc	2019	\N	\N	f	2012	56	308.405	https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.webp	static/circuit_images/USA_Circuit.webp
\.


--
-- Data for Name: constructor_standings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.constructor_standings (id, season_id, constructor_id, "position", points, wins, position_text) FROM stdin;
91	3	mclaren	1	460	9	1
92	3	ferrari	2	222	0	2
93	3	mercedes	3	210	1	3
94	3	red_bull	4	172	2	4
95	3	williams	5	59	0	5
96	3	sauber	6	41	0	6
97	3	rb	7	36	0	7
98	3	aston_martin	8	36	0	8
99	3	haas	9	29	0	9
100	3	alpine	10	19	0	10
51	2	mclaren	1	666	6	1
52	2	ferrari	2	652	5	2
53	2	red_bull	3	589	9	3
54	2	mercedes	4	468	4	4
55	2	aston_martin	5	94	0	5
56	2	alpine	6	65	0	6
57	2	haas	7	58	0	7
58	2	rb	8	46	0	8
59	2	williams	9	17	0	9
60	2	sauber	10	4	0	10
\.


--
-- Data for Name: constructors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.constructors (constructor_id, constructor_url, constructor_name, constructor_nationality, season_id, base, team_chief, technical_chief, power_unit, is_active, championships, wins, podiums, poles, fastest_laps) FROM stdin;
alpine	http://en.wikipedia.org/wiki/Alpine_F1_Team	Alpine F1 Team	French	3	\N	\N	\N	\N	t	0	0	0	0	0
aston_martin	http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One	Aston Martin	British	3	\N	\N	\N	\N	t	0	0	0	0	0
ferrari	http://en.wikipedia.org/wiki/Scuderia_Ferrari	Ferrari	Italian	3	\N	\N	\N	\N	t	0	0	0	0	0
haas	http://en.wikipedia.org/wiki/Haas_F1_Team	Haas F1 Team	American	3	\N	\N	\N	\N	t	0	0	0	0	0
mclaren	http://en.wikipedia.org/wiki/McLaren	McLaren	British	3	\N	\N	\N	\N	t	0	0	0	0	0
mercedes	http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One	Mercedes	German	3	\N	\N	\N	\N	t	0	0	0	0	0
rb	http://en.wikipedia.org/wiki/RB_Formula_One_Team	RB F1 Team	Italian	3	\N	\N	\N	\N	t	0	0	0	0	0
red_bull	http://en.wikipedia.org/wiki/Red_Bull_Racing	Red Bull	Austrian	3	\N	\N	\N	\N	t	0	0	0	0	0
sauber	http://en.wikipedia.org/wiki/Sauber_Motorsport	Sauber	Swiss	3	\N	\N	\N	\N	t	0	0	0	0	0
williams	http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering	Williams	British	3	\N	\N	\N	\N	t	0	0	0	0	0
\.


--
-- Data for Name: driver_seasons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.driver_seasons (id, driver_id, constructor_id, season_id) FROM stdin;
41	lawson	rb	3
42	tsunoda	red_bull	3
\.


--
-- Data for Name: driver_standings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.driver_standings (id, season_id, driver_id, constructor_id, "position", points, wins, position_text) FROM stdin;
85	2	max_verstappen	red_bull	1	437	9	1
86	2	norris	mclaren	2	374	4	2
87	2	leclerc	ferrari	3	356	3	3
88	2	piastri	mclaren	4	292	2	4
89	2	sainz	ferrari	5	290	2	5
90	2	russell	mercedes	6	245	2	6
91	2	hamilton	mercedes	7	223	2	7
92	2	perez	red_bull	8	152	0	8
93	2	alonso	aston_martin	9	70	0	9
94	2	gasly	alpine	10	42	0	10
95	2	hulkenberg	haas	11	41	0	11
96	2	tsunoda	rb	12	30	0	12
97	2	stroll	aston_martin	13	24	0	13
98	2	ocon	alpine	14	23	0	14
99	2	kevin_magnussen	haas	15	16	0	15
100	2	albon	williams	16	12	0	16
101	2	ricciardo	rb	17	12	0	17
102	2	bearman	ferrari	18	7	0	18
103	2	colapinto	williams	19	5	0	19
104	2	zhou	sauber	20	4	0	20
105	2	lawson	rb	21	4	0	21
106	2	bottas	sauber	22	0	0	22
107	2	sargeant	williams	23	0	0	23
108	2	doohan	alpine	24	0	0	24
172	3	piastri	mclaren	1	234	5	1
173	3	norris	mclaren	2	226	4	2
174	3	max_verstappen	red_bull	3	165	2	3
175	3	russell	mercedes	4	147	1	4
176	3	leclerc	ferrari	5	119	0	5
177	3	hamilton	ferrari	6	103	0	6
178	3	antonelli	mercedes	7	63	0	7
179	3	albon	williams	8	46	0	8
180	3	hulkenberg	sauber	9	37	0	9
181	3	ocon	haas	10	23	0	10
182	3	hadjar	rb	11	21	0	11
183	3	stroll	aston_martin	12	20	0	12
184	3	gasly	alpine	13	19	0	13
185	3	alonso	aston_martin	14	16	0	14
186	3	sainz	williams	15	13	0	15
187	3	lawson	red_bull	16	12	0	16
188	3	tsunoda	rb	17	10	0	17
189	3	bearman	haas	18	6	0	18
190	3	bortoleto	sauber	19	4	0	19
191	3	colapinto	alpine	20	0	0	20
192	3	doohan	alpine	21	0	0	21
\.


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.drivers (driver_id, driver_number, driver_code, driver_url, given_name, family_name, date_of_birth, driver_nationality) FROM stdin;
albon	23	ALB	http://en.wikipedia.org/wiki/Alexander_Albon	Alexander	Albon	1996-03-23	Thai
alonso	14	ALO	http://en.wikipedia.org/wiki/Fernando_Alonso	Fernando	Alonso	1981-07-29	Spanish
antonelli	12	ANT	https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli	Andrea Kimi	Antonelli	2006-08-25	Italian
bearman	87	BEA	http://en.wikipedia.org/wiki/Oliver_Bearman	Oliver	Bearman	2005-05-08	British
bortoleto	5	BOR	https://en.wikipedia.org/wiki/Gabriel_Bortoleto	Gabriel	Bortoleto	2004-10-14	Brazilian
colapinto	43	COL	http://en.wikipedia.org/wiki/Franco_Colapinto	Franco	Colapinto	2003-05-27	Argentine
doohan	7	DOO	http://en.wikipedia.org/wiki/Jack_Doohan	Jack	Doohan	2003-01-20	Australian
gasly	10	GAS	http://en.wikipedia.org/wiki/Pierre_Gasly	Pierre	Gasly	1996-02-07	French
hadjar	6	HAD	https://en.wikipedia.org/wiki/Isack_Hadjar	Isack	Hadjar	2004-09-28	French
hamilton	44	HAM	http://en.wikipedia.org/wiki/Lewis_Hamilton	Lewis	Hamilton	1985-01-07	British
hulkenberg	27	HUL	http://en.wikipedia.org/wiki/Nico_H%C3%BClkenberg	Nico	Hülkenberg	1987-08-19	German
lawson	30	LAW	http://en.wikipedia.org/wiki/Liam_Lawson	Liam	Lawson	2002-02-11	New Zealander
leclerc	16	LEC	http://en.wikipedia.org/wiki/Charles_Leclerc	Charles	Leclerc	1997-10-16	Monegasque
norris	4	NOR	http://en.wikipedia.org/wiki/Lando_Norris	Lando	Norris	1999-11-13	British
ocon	31	OCO	http://en.wikipedia.org/wiki/Esteban_Ocon	Esteban	Ocon	1996-09-17	French
piastri	81	PIA	http://en.wikipedia.org/wiki/Oscar_Piastri	Oscar	Piastri	2001-04-06	Australian
russell	63	RUS	http://en.wikipedia.org/wiki/George_Russell_(racing_driver)	George	Russell	1998-02-15	British
sainz	55	SAI	http://en.wikipedia.org/wiki/Carlos_Sainz_Jr.	Carlos	Sainz	1994-09-01	Spanish
stroll	18	STR	http://en.wikipedia.org/wiki/Lance_Stroll	Lance	Stroll	1998-10-29	Canadian
tsunoda	22	TSU	http://en.wikipedia.org/wiki/Yuki_Tsunoda	Yuki	Tsunoda	2000-05-11	Japanese
max_verstappen	33	VER	http://en.wikipedia.org/wiki/Max_Verstappen	Max	Verstappen	1997-09-30	Dutch
perez	11	PER	http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez	Sergio	Pérez	1990-01-26	Mexican
kevin_magnussen	20	MAG	http://en.wikipedia.org/wiki/Kevin_Magnussen	Kevin	Magnussen	1992-10-05	Danish
ricciardo	3	RIC	http://en.wikipedia.org/wiki/Daniel_Ricciardo	Daniel	Ricciardo	1989-07-01	Australian
zhou	24	ZHO	http://en.wikipedia.org/wiki/Zhou_Guanyu	Guanyu	Zhou	1999-05-30	Chinese
bottas	77	BOT	http://en.wikipedia.org/wiki/Valtteri_Bottas	Valtteri	Bottas	1989-08-28	Finnish
sargeant	2	SAR	http://en.wikipedia.org/wiki/Logan_Sargeant	Logan	Sargeant	2000-12-31	American
\.


--
-- Data for Name: qualifying_results; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.qualifying_results (id, race_id, driver_id, constructor_id, number, "position", q1_time, q2_time, q3_time) FROM stdin;
201	18	norris	mclaren	4	1	0 days 00:01:04.672000	0 days 00:01:04.410000	0 days 00:01:03.971000
202	18	leclerc	ferrari	16	2	0 days 00:01:05.197000	0 days 00:01:04.734000	0 days 00:01:04.492000
203	18	piastri	mclaren	81	3	0 days 00:01:04.966000	0 days 00:01:04.556000	0 days 00:01:04.554000
204	18	hamilton	ferrari	44	4	0 days 00:01:05.115000	0 days 00:01:04.896000	0 days 00:01:04.582000
205	18	russell	mercedes	63	5	0 days 00:01:05.189000	0 days 00:01:04.860000	0 days 00:01:04.763000
206	18	lawson	rb	30	6	0 days 00:01:05.017000	0 days 00:01:05.041000	0 days 00:01:04.926000
207	18	max_verstappen	red_bull	1	7	0 days 00:01:05.106000	0 days 00:01:04.836000	0 days 00:01:04.929000
208	18	bortoleto	sauber	5	8	0 days 00:01:05.123000	0 days 00:01:04.846000	0 days 00:01:05.132000
209	18	gasly	alpine	10	10	0 days 00:01:05.054000	0 days 00:01:04.846000	0 days 00:01:05.649000
210	18	hadjar	rb	6	13	0 days 00:01:05.063000	0 days 00:01:05.226000	\N
211	18	antonelli	mercedes	12	9	0 days 00:01:05.178000	0 days 00:01:05.052000	0 days 00:01:05.276000
212	18	alonso	aston_martin	14	11	0 days 00:01:05.197000	0 days 00:01:05.128000	\N
213	18	albon	williams	23	12	0 days 00:01:05.143000	0 days 00:01:05.205000	\N
214	18	colapinto	alpine	43	14	0 days 00:01:05.278000	0 days 00:01:05.288000	\N
215	18	bearman	haas	87	15	0 days 00:01:05.218000	0 days 00:01:05.312000	\N
216	18	stroll	aston_martin	18	16	0 days 00:01:05.329000	\N	\N
217	18	ocon	haas	31	17	0 days 00:01:05.364000	\N	\N
218	18	tsunoda	red_bull	22	18	0 days 00:01:05.369000	\N	\N
219	18	sainz	williams	55	19	0 days 00:01:05.582000	\N	\N
220	18	hulkenberg	sauber	27	20	0 days 00:01:05.606000	\N	\N
221	7	max_verstappen	red_bull	1	1	0 days 00:01:25.886000	0 days 00:01:25.316000	0 days 00:01:24.892000
222	7	piastri	mclaren	81	2	0 days 00:01:25.963000	0 days 00:01:25.316000	0 days 00:01:24.995000
223	7	norris	mclaren	4	3	0 days 00:01:26.123000	0 days 00:01:25.231000	0 days 00:01:25.010000
224	7	russell	mercedes	63	4	0 days 00:01:26.236000	0 days 00:01:25.637000	0 days 00:01:25.029000
225	7	hamilton	ferrari	44	5	0 days 00:01:26.296000	0 days 00:01:25.084000	0 days 00:01:25.095000
226	7	leclerc	ferrari	16	6	0 days 00:01:26.186000	0 days 00:01:25.133000	0 days 00:01:25.121000
227	7	antonelli	mercedes	12	7	0 days 00:01:26.265000	0 days 00:01:25.620000	0 days 00:01:25.374000
228	7	bearman	haas	87	8	0 days 00:01:26.005000	0 days 00:01:25.534000	0 days 00:01:25.471000
229	7	alonso	aston_martin	14	9	0 days 00:01:26.108000	0 days 00:01:25.593000	0 days 00:01:25.621000
230	7	gasly	alpine	10	10	0 days 00:01:26.328000	0 days 00:01:25.711000	0 days 00:01:25.785000
231	7	sainz	williams	55	11	0 days 00:01:26.175000	0 days 00:01:25.746000	\N
232	7	tsunoda	red_bull	22	12	0 days 00:01:26.275000	0 days 00:01:25.826000	\N
233	7	hadjar	rb	6	13	0 days 00:01:26.177000	0 days 00:01:25.864000	\N
234	7	albon	williams	23	14	0 days 00:01:26.093000	0 days 00:01:25.889000	\N
235	7	ocon	haas	31	15	0 days 00:01:26.136000	0 days 00:01:25.950000	\N
236	7	lawson	rb	30	16	0 days 00:01:26.440000	\N	\N
237	7	bortoleto	sauber	5	17	0 days 00:01:26.446000	\N	\N
238	7	stroll	aston_martin	18	18	0 days 00:01:26.504000	\N	\N
239	7	hulkenberg	sauber	27	19	0 days 00:01:26.574000	\N	\N
240	7	colapinto	alpine	43	20	0 days 00:01:27.060000	\N	\N
241	14	norris	mclaren	4	1			
242	14	piastri	mclaren	81	2			
243	14	max_verstappen	red_bull	1	3			
244	14	russell	mercedes	63	4			
245	14	tsunoda	rb	22	5			
246	14	albon	williams	23	6			
247	14	leclerc	ferrari	16	7			
248	14	hamilton	ferrari	44	8			
249	14	gasly	alpine	10	9			
250	14	sainz	williams	55	10			
251	14	hadjar	rb	6	11			
252	14	alonso	aston_martin	14	12			
253	14	stroll	aston_martin	18	13			
254	14	doohan	alpine	7	14			
255	14	bortoleto	sauber	5	15			
256	14	antonelli	mercedes	12	16			
257	14	hulkenberg	sauber	27	17			
258	14	lawson	red_bull	30	18			
259	14	ocon	haas	31	19			
260	14	bearman	haas	87	20			
261	1	piastri	mclaren	81	1			
262	1	russell	mercedes	63	2			
263	1	norris	mclaren	4	3			
264	1	max_verstappen	red_bull	1	4			
265	1	hamilton	ferrari	44	5			
266	1	leclerc	ferrari	16	6			
267	1	hadjar	rb	6	7			
268	1	antonelli	mercedes	12	8			
269	1	tsunoda	rb	22	9			
270	1	albon	williams	23	10			
271	1	ocon	haas	31	11			
272	1	hulkenberg	sauber	27	12			
273	1	alonso	aston_martin	14	13			
274	1	stroll	aston_martin	18	14			
275	1	sainz	williams	55	15			
276	1	gasly	alpine	10	16			
277	1	bearman	haas	87	17			
278	1	doohan	alpine	7	18			
279	1	bortoleto	sauber	5	19			
280	1	lawson	red_bull	30	20			
281	2	max_verstappen	red_bull	1	1			
282	2	norris	mclaren	4	2			
283	2	piastri	mclaren	81	3			
284	2	leclerc	ferrari	16	4			
285	2	russell	mercedes	63	5			
286	2	antonelli	mercedes	12	6			
287	2	hadjar	rb	6	7			
288	2	hamilton	ferrari	44	8			
289	2	albon	williams	23	9			
290	2	bearman	haas	87	10			
291	2	gasly	alpine	10	11			
292	2	sainz	williams	55	12			
293	2	alonso	aston_martin	14	13			
294	2	lawson	rb	30	14			
295	2	tsunoda	red_bull	22	15			
296	2	hulkenberg	sauber	27	16			
297	2	bortoleto	sauber	5	17			
298	2	ocon	haas	31	18			
299	2	doohan	alpine	7	19			
300	2	stroll	aston_martin	18	20			
301	15	piastri	mclaren	81	1			
302	15	russell	mercedes	63	2			
303	15	leclerc	ferrari	16	3			
304	15	antonelli	mercedes	12	4			
305	15	gasly	alpine	10	5			
306	15	norris	mclaren	4	6			
307	15	max_verstappen	red_bull	1	7			
308	15	sainz	williams	55	8			
309	15	hamilton	ferrari	44	9			
310	15	tsunoda	red_bull	22	10			
311	15	doohan	alpine	7	11			
312	15	hadjar	rb	6	12			
313	15	alonso	aston_martin	14	13			
314	15	ocon	haas	31	14			
315	15	albon	williams	23	15			
316	15	hulkenberg	sauber	27	16			
317	15	lawson	rb	30	17			
318	15	bortoleto	sauber	5	18			
319	15	stroll	aston_martin	18	19			
320	15	bearman	haas	87	20			
321	3	max_verstappen	red_bull	1	1			
322	3	piastri	mclaren	81	2			
323	3	russell	mercedes	63	3			
324	3	leclerc	ferrari	16	4			
325	3	antonelli	mercedes	12	5			
326	3	sainz	williams	55	6			
327	3	hamilton	ferrari	44	7			
328	3	tsunoda	red_bull	22	8			
329	3	gasly	alpine	10	9			
330	3	norris	mclaren	4	10			
331	3	albon	williams	23	11			
332	3	lawson	rb	30	12			
333	3	alonso	aston_martin	14	13			
334	3	hadjar	rb	6	14			
335	3	bearman	haas	87	15			
336	3	stroll	aston_martin	18	16			
337	3	doohan	alpine	7	17			
338	3	hulkenberg	sauber	27	18			
339	3	ocon	haas	31	19			
340	3	bortoleto	sauber	5	20			
341	4	max_verstappen	red_bull	1	1			
342	4	norris	mclaren	4	2			
343	4	antonelli	mercedes	12	3			
344	4	piastri	mclaren	81	4			
345	4	russell	mercedes	63	5			
346	4	sainz	williams	55	6			
347	4	albon	williams	23	7			
348	4	leclerc	ferrari	16	8			
349	4	ocon	haas	31	9			
350	4	tsunoda	red_bull	22	10			
351	4	hadjar	rb	6	11			
352	4	hamilton	ferrari	44	12			
353	4	bortoleto	sauber	5	13			
354	4	doohan	alpine	7	14			
355	4	lawson	rb	30	15			
356	4	hulkenberg	sauber	27	16			
357	4	alonso	aston_martin	14	17			
358	4	gasly	alpine	10	18			
359	4	stroll	aston_martin	18	19			
360	4	bearman	haas	87	20			
361	16	piastri	mclaren	81	1			
362	16	max_verstappen	red_bull	1	2			
363	16	russell	mercedes	63	3			
364	16	norris	mclaren	4	4			
365	16	alonso	aston_martin	14	5			
366	16	sainz	williams	55	6			
367	16	albon	williams	23	7			
368	16	stroll	aston_martin	18	8			
369	16	hadjar	rb	6	9			
370	16	gasly	alpine	10	10			
371	16	leclerc	ferrari	16	11			
372	16	hamilton	ferrari	44	12			
373	16	antonelli	mercedes	12	13			
374	16	bortoleto	sauber	5	14			
375	16	colapinto	alpine	43	15			
376	16	lawson	rb	30	16			
377	16	hulkenberg	sauber	27	17			
378	16	ocon	haas	31	18			
379	16	bearman	haas	87	19			
380	16	tsunoda	red_bull	22	20			
381	5	norris	mclaren	4	1			
382	5	leclerc	ferrari	16	2			
383	5	piastri	mclaren	81	3			
384	5	hamilton	ferrari	44	4			
385	5	max_verstappen	red_bull	1	5			
386	5	hadjar	rb	6	6			
387	5	alonso	aston_martin	14	7			
388	5	ocon	haas	31	8			
389	5	lawson	rb	30	9			
390	5	albon	williams	23	10			
391	5	sainz	williams	55	11			
392	5	tsunoda	red_bull	22	12			
393	5	hulkenberg	sauber	27	13			
394	5	russell	mercedes	63	14			
395	5	antonelli	mercedes	12	15			
396	5	bortoleto	sauber	5	16			
397	5	bearman	haas	87	17			
398	5	gasly	alpine	10	18			
399	5	stroll	aston_martin	18	19			
400	5	colapinto	alpine	43	20			
401	6	piastri	mclaren	81	1			
402	6	norris	mclaren	4	2			
403	6	max_verstappen	red_bull	1	3			
404	6	russell	mercedes	63	4			
405	6	hamilton	ferrari	44	5			
406	6	antonelli	mercedes	12	6			
407	6	leclerc	ferrari	16	7			
408	6	gasly	alpine	10	8			
409	6	hadjar	rb	6	9			
410	6	alonso	aston_martin	14	10			
411	6	albon	williams	23	11			
412	6	bortoleto	sauber	5	12			
413	6	lawson	rb	30	13			
414	6	stroll	aston_martin	18	14			
415	6	bearman	haas	87	15			
416	6	hulkenberg	sauber	27	16			
417	6	ocon	haas	31	17			
418	6	sainz	williams	55	18			
419	6	colapinto	alpine	43	19			
420	6	tsunoda	red_bull	22	20			
421	17	russell	mercedes	63	1			
422	17	max_verstappen	red_bull	1	2			
423	17	piastri	mclaren	81	3			
424	17	antonelli	mercedes	12	4			
425	17	hamilton	ferrari	44	5			
426	17	alonso	aston_martin	14	6			
427	17	norris	mclaren	4	7			
428	17	leclerc	ferrari	16	8			
429	17	hadjar	rb	6	9			
430	17	albon	williams	23	10			
431	17	tsunoda	red_bull	22	11			
432	17	colapinto	alpine	43	12			
433	17	hulkenberg	sauber	27	13			
434	17	bearman	haas	87	14			
435	17	ocon	haas	31	15			
436	17	bortoleto	sauber	5	16			
437	17	sainz	williams	55	17			
438	17	stroll	aston_martin	18	18			
439	17	lawson	rb	30	19			
440	17	gasly	alpine	10	20			
\.


--
-- Data for Name: races; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.races (id, season_id, circuit_id, round_number, country, location, official_event_name, event_date, event_format, session1, session1_date, session2, session2_date, session3, session3_date, session4, session4_date, session5, session5_date, is_sprint) FROM stdin;
4	3	miami	6	United States	Miami	Miami Grand Prix	2025-05-04	sprint_qualifying	Practice 1	2025-05-02 16:30:00	Sprint Qualifying	2025-05-02 20:30:00	Sprint	2025-05-03 16:00:00	Qualifying	2025-05-03 20:00:00	Race	2025-05-04 20:00:00	t
5	3	monaco	8	Monaco	Monaco	Monaco Grand Prix	2025-05-25	conventional	Practice 1	2025-05-23 11:30:00	Practice 2	2025-05-23 15:00:00	Practice 3	2025-05-24 10:30:00	Qualifying	2025-05-24 14:00:00	Race	2025-05-25 13:00:00	f
6	3	catalunya	9	Spain	Barcelona	Spanish Grand Prix	2025-06-01	conventional	Practice 1	2025-05-30 11:30:00	Practice 2	2025-05-30 15:00:00	Practice 3	2025-05-31 10:30:00	Qualifying	2025-05-31 14:00:00	Race	2025-06-01 13:00:00	f
7	3	silverstone	12	United Kingdom	Silverstone	British Grand Prix	2025-07-06	conventional	Practice 1	2025-07-04 11:30:00	Practice 2	2025-07-04 15:00:00	Practice 3	2025-07-05 10:30:00	Qualifying	2025-07-05 14:00:00	Race	2025-07-06 14:00:00	f
8	3	spa	13	Belgium	Spa-Francorchamps	Belgian Grand Prix	2025-07-27	sprint_qualifying	Practice 1	2025-07-25 10:30:00	Sprint Qualifying	2025-07-25 14:30:00	Sprint	2025-07-26 10:00:00	Qualifying	2025-07-26 14:00:00	Race	2025-07-27 13:00:00	t
1	3	shanghai	2	China	Shanghai	Chinese Grand Prix	2025-03-23	sprint_qualifying	Practice 1	2025-03-21 03:30:00	Sprint Qualifying	2025-03-21 07:30:00	Sprint	2025-03-22 03:00:00	Qualifying	2025-03-22 07:00:00	Race	2025-03-23 07:00:00	t
2	3	suzuka	3	Japan	Suzuka	Japanese Grand Prix	2025-04-06	conventional	Practice 1	2025-04-04 02:30:00	Practice 2	2025-04-04 06:00:00	Practice 3	2025-04-05 02:30:00	Qualifying	2025-04-05 06:00:00	Race	2025-04-06 05:00:00	f
3	3	jeddah	5	Saudi Arabia	Jeddah	Saudi Arabian Grand Prix	2025-04-20	conventional	Practice 1	2025-04-18 13:30:00	Practice 2	2025-04-18 17:00:00	Practice 3	2025-04-19 13:30:00	Qualifying	2025-04-19 17:00:00	Race	2025-04-20 17:00:00	f
9	3	zandvoort	15	Netherlands	Zandvoort	Dutch Grand Prix	2025-08-31	conventional	Practice 1	2025-08-29 10:30:00	Practice 2	2025-08-29 14:00:00	Practice 3	2025-08-30 09:30:00	Qualifying	2025-08-30 13:00:00	Race	2025-08-31 13:00:00	f
25	3	bahrain	0	Bahrain	Sakhir	FORMULA 1 ARAMCO PRE-SEASON TESTING 2025	2025-02-28	testing	Practice 1	2025-02-26 07:00:00	Practice 2	2025-02-27 07:00:00	Practice 3	2025-02-28 07:00:00	None	\N	None	\N	f
20	3	americas	19	United States	Austin	United States Grand Prix	2025-10-19	sprint_qualifying	Practice 1	2025-10-17 17:30:00	Sprint Qualifying	2025-10-17 21:30:00	Sprint	2025-10-18 17:00:00	Qualifying	2025-10-18 21:00:00	Race	2025-10-19 19:00:00	t
13	3	vegas	22	United States	Las Vegas	Las Vegas Grand Prix	2025-11-22	conventional	Practice 1	2025-11-21 00:30:00	Practice 2	2025-11-21 04:00:00	Practice 3	2025-11-22 00:30:00	Qualifying	2025-11-22 04:00:00	Race	2025-11-23 04:00:00	f
17	3	villeneuve	10	Canada	Montréal	Canadian Grand Prix	2025-06-15	conventional	Practice 1	2025-06-13 17:30:00	Practice 2	2025-06-13 21:00:00	Practice 3	2025-06-14 16:30:00	Qualifying	2025-06-14 20:00:00	Race	2025-06-15 18:00:00	f
23	3	losail	23	Qatar	Lusail	Qatar Grand Prix	2025-11-30	sprint_qualifying	Practice 1	2025-11-28 13:30:00	Sprint Qualifying	2025-11-28 17:30:00	Sprint	2025-11-29 14:00:00	Qualifying	2025-11-29 18:00:00	Race	2025-11-30 16:00:00	t
24	3	yas_marina	24	United Arab Emirates	Yas Island	Abu Dhabi Grand Prix	2025-12-07	conventional	Practice 1	2025-12-05 09:30:00	Practice 2	2025-12-05 13:00:00	Practice 3	2025-12-06 10:30:00	Qualifying	2025-12-06 14:00:00	Race	2025-12-07 13:00:00	f
10	3	monza	16	Italy	Monza	Italian Grand Prix	2025-09-07	conventional	Practice 1	2025-09-05 11:30:00	Practice 2	2025-09-05 15:00:00	Practice 3	2025-09-06 10:30:00	Qualifying	2025-09-06 14:00:00	Race	2025-09-07 13:00:00	f
11	3	baku	17	Azerbaijan	Baku	Azerbaijan Grand Prix	2025-09-21	conventional	Practice 1	2025-09-19 08:30:00	Practice 2	2025-09-19 12:00:00	Practice 3	2025-09-20 08:30:00	Qualifying	2025-09-20 12:00:00	Race	2025-09-21 11:00:00	f
12	3	marina_bay	18	Singapore	Marina Bay	Singapore Grand Prix	2025-10-05	conventional	Practice 1	2025-10-03 09:30:00	Practice 2	2025-10-03 13:00:00	Practice 3	2025-10-04 09:30:00	Qualifying	2025-10-04 13:00:00	Race	2025-10-05 12:00:00	f
14	3	albert_park	1	Australia	Melbourne	Australian Grand Prix	2025-03-16	conventional	Practice 1	2025-03-14 01:30:00	Practice 2	2025-03-14 05:00:00	Practice 3	2025-03-15 01:30:00	Qualifying	2025-03-15 05:00:00	Race	2025-03-16 04:00:00	f
15	3	bahrain	4	Bahrain	Sakhir	Bahrain Grand Prix	2025-04-13	conventional	Practice 1	2025-04-11 11:30:00	Practice 2	2025-04-11 15:00:00	Practice 3	2025-04-12 12:30:00	Qualifying	2025-04-12 16:00:00	Race	2025-04-13 15:00:00	f
16	3	imola	7	Italy	Imola	Emilia Romagna Grand Prix	2025-05-18	conventional	Practice 1	2025-05-16 11:30:00	Practice 2	2025-05-16 15:00:00	Practice 3	2025-05-17 10:30:00	Qualifying	2025-05-17 14:00:00	Race	2025-05-18 13:00:00	f
18	3	red_bull_ring	11	Austria	Spielberg	Austrian Grand Prix	2025-06-29	conventional	Practice 1	2025-06-27 11:30:00	Practice 2	2025-06-27 15:00:00	Practice 3	2025-06-28 10:30:00	Qualifying	2025-06-28 14:00:00	Race	2025-06-29 13:00:00	f
19	3	hungaroring	14	Hungary	Budapest	Hungarian Grand Prix	2025-08-03	conventional	Practice 1	2025-08-01 11:30:00	Practice 2	2025-08-01 15:00:00	Practice 3	2025-08-02 10:30:00	Qualifying	2025-08-02 14:00:00	Race	2025-08-03 13:00:00	f
21	3	rodriguez	20	Mexico	Mexico City	Mexico City Grand Prix	2025-10-26	conventional	Practice 1	2025-10-24 18:30:00	Practice 2	2025-10-24 22:00:00	Practice 3	2025-10-25 17:30:00	Qualifying	2025-10-25 21:00:00	Race	2025-10-26 20:00:00	f
22	3	interlagos	21	Brazil	São Paulo	São Paulo Grand Prix	2025-11-09	sprint_qualifying	Practice 1	2025-11-07 14:30:00	Sprint Qualifying	2025-11-07 18:30:00	Sprint	2025-11-08 14:00:00	Qualifying	2025-11-08 18:00:00	Race	2025-11-09 17:00:00	t
\.


--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.results (id, race_id, driver_id, constructor_id, number, "position", position_text, points, grid, laps, status, total_race_time_millis, total_race_time, fastest_lap_rank, fastest_lap_number, fastest_lap_time) FROM stdin;
1	14	norris	mclaren	4	1	1	25	1	57	Finished	6126304	0 days 01:42:06.304000	1	43	0 days 00:01:22.167000
2	14	max_verstappen	red_bull	1	2	2	18	3	57	Finished	6127199	0 days 00:00:00.895000	3	43	0 days 00:01:23.081000
3	14	russell	mercedes	63	3	3	15	4	57	Finished	6134785	0 days 00:00:08.481000	11	43	0 days 00:01:25.065000
4	14	antonelli	mercedes	12	4	4	12	16	57	Finished	6136439	0 days 00:00:10.135000	9	43	0 days 00:01:24.901000
5	14	albon	williams	23	5	5	10	6	57	Finished	6139077	0 days 00:00:12.773000	8	43	0 days 00:01:24.597000
6	14	stroll	aston_martin	18	6	6	8	13	57	Finished	6143717	0 days 00:00:17.413000	14	43	0 days 00:01:25.538000
7	14	hulkenberg	sauber	27	7	7	6	17	57	Finished	6144727	0 days 00:00:18.423000	12	43	0 days 00:01:25.243000
8	14	leclerc	ferrari	16	8	8	4	7	57	Finished	6146130	0 days 00:00:19.826000	13	43	0 days 00:01:25.271000
9	14	piastri	mclaren	81	9	9	2	2	57	Finished	6146752	0 days 00:00:20.448000	4	43	0 days 00:01:23.242000
10	14	hamilton	ferrari	44	10	10	1	8	57	Finished	6148777	0 days 00:00:22.473000	7	43	0 days 00:01:24.218000
11	14	gasly	alpine	10	11	11	0	9	57	Finished	6152806	0 days 00:00:26.502000	10	43	0 days 00:01:25.020000
12	14	tsunoda	rb	22	12	12	0	5	57	Finished	6156188	0 days 00:00:29.884000	6	43	0 days 00:01:24.194000
13	14	ocon	haas	31	13	13	0	19	57	Finished	6159465	0 days 00:00:33.161000	15	42	0 days 00:01:26.764000
14	14	bearman	haas	87	14	14	0	20	57	Finished	6166655	0 days 00:00:40.351000	16	42	0 days 00:01:27.603000
15	14	lawson	red_bull	30	15	R	0	18	46	Retired	\N	\N	2	43	0 days 00:01:22.970000
16	14	bortoleto	sauber	5	16	R	0	15	45	Retired	\N	\N	5	43	0 days 00:01:24.192000
17	14	alonso	aston_martin	14	17	R	0	12	32	Retired	\N	\N	17	32	0 days 00:01:28.819000
18	14	sainz	williams	55	18	R	0	10	0	Retired	\N	\N	\N	\N	\N
19	14	doohan	alpine	7	19	R	0	14	0	Retired	\N	\N	\N	\N	\N
20	14	hadjar	rb	6	20	R	0	11	0	Retired	\N	\N	\N	\N	\N
21	1	piastri	mclaren	81	1	1	25	1	56	Finished	5455026	0 days 01:30:55.026000	3	53	0 days 00:01:35.520000
22	1	norris	mclaren	4	2	2	18	3	56	Finished	5464774	0 days 00:00:09.748000	1	53	0 days 00:01:35.454000
23	1	russell	mercedes	63	3	3	15	2	56	Finished	5466123	0 days 00:00:11.097000	5	55	0 days 00:01:35.816000
24	1	max_verstappen	red_bull	1	4	4	12	4	56	Finished	5471682	0 days 00:00:16.656000	2	56	0 days 00:01:35.488000
25	1	ocon	haas	31	5	5	10	11	56	Finished	5504995	0 days 00:00:49.969000	4	56	0 days 00:01:35.740000
26	1	antonelli	mercedes	12	6	6	8	8	56	Finished	5508774	0 days 00:00:53.748000	11	56	0 days 00:01:36.046000
27	1	albon	williams	23	7	7	6	10	56	Finished	5511347	0 days 00:00:56.321000	12	52	0 days 00:01:36.254000
28	1	bearman	haas	87	8	8	4	17	56	Finished	5516329	0 days 00:01:01.303000	13	52	0 days 00:01:36.363000
29	1	stroll	aston_martin	18	9	9	2	14	56	Finished	5525230	0 days 00:01:10.204000	10	39	0 days 00:01:36.044000
30	1	sainz	williams	55	10	10	1	15	56	Finished	5531413	0 days 00:01:16.387000	15	50	0 days 00:01:36.779000
31	1	hadjar	rb	6	11	11	0	7	56	Finished	5533901	0 days 00:01:18.875000	6	35	0 days 00:01:35.868000
32	1	lawson	red_bull	30	12	12	0	20	56	Finished	5536173	0 days 00:01:21.147000	9	32	0 days 00:01:35.985000
33	1	doohan	alpine	7	13	13	0	18	56	Finished	5543427	0 days 00:01:28.401000	14	52	0 days 00:01:36.424000
34	1	bortoleto	sauber	5	14	14	0	19	55	Lapped	5465782	0 days 00:00:10.756000	8	28	0 days 00:01:35.874000
35	1	hulkenberg	sauber	27	15	15	0	12	55	Lapped	5475252	0 days 00:00:20.226000	16	35	0 days 00:01:37.275000
36	1	tsunoda	rb	22	16	16	0	9	55	Lapped	5478537	0 days 00:00:23.511000	7	49	0 days 00:01:35.871000
37	1	alonso	aston_martin	14	17	R	0	13	4	Retired	\N	\N	17	3	0 days 00:01:39.256000
38	1	leclerc	ferrari	16	18	D	0	6	0	Disqualified	\N	\N	\N	\N	\N
39	1	hamilton	ferrari	44	19	D	0	5	0	Disqualified	\N	\N	\N	\N	\N
40	1	gasly	alpine	10	20	D	0	16	0	Disqualified	\N	\N	\N	\N	\N
41	2	max_verstappen	red_bull	1	1	1	25	1	53	Finished	4926983	0 days 01:22:06.983000	3	52	0 days 00:01:31.041000
42	2	norris	mclaren	4	2	2	18	2	53	Finished	4928406	0 days 00:00:01.423000	5	51	0 days 00:01:31.116000
43	2	piastri	mclaren	81	3	3	15	3	53	Finished	4929112	0 days 00:00:02.129000	2	53	0 days 00:01:31.039000
44	2	leclerc	ferrari	16	4	4	12	4	53	Finished	4943080	0 days 00:00:16.097000	10	47	0 days 00:01:31.469000
45	2	russell	mercedes	63	5	5	10	5	53	Finished	4944345	0 days 00:00:17.362000	8	51	0 days 00:01:31.357000
46	2	antonelli	mercedes	12	6	6	8	6	53	Finished	4945654	0 days 00:00:18.671000	1	50	0 days 00:01:30.965000
47	2	hamilton	ferrari	44	7	7	6	8	53	Finished	4956165	0 days 00:00:29.182000	9	51	0 days 00:01:31.406000
48	2	hadjar	rb	6	8	8	4	7	53	Finished	4964117	0 days 00:00:37.134000	7	52	0 days 00:01:31.317000
49	2	albon	williams	23	9	9	2	9	53	Finished	4967350	0 days 00:00:40.367000	6	52	0 days 00:01:31.125000
50	2	bearman	haas	87	10	10	1	10	53	Finished	4981512	0 days 00:00:54.529000	15	49	0 days 00:01:32.006000
51	2	alonso	aston_martin	14	11	11	0	12	53	Finished	4984316	0 days 00:00:57.333000	11	51	0 days 00:01:31.770000
52	2	tsunoda	red_bull	22	12	12	0	14	53	Finished	4985384	0 days 00:00:58.401000	13	51	0 days 00:01:31.871000
53	2	gasly	alpine	10	13	13	0	11	53	Finished	4989105	0 days 00:01:02.122000	12	52	0 days 00:01:31.820000
54	2	sainz	williams	55	14	14	0	15	53	Finished	5001112	0 days 00:01:14.129000	4	36	0 days 00:01:31.106000
55	2	doohan	alpine	7	15	15	0	19	53	Finished	5008297	0 days 00:01:21.314000	20	47	0 days 00:01:32.685000
56	2	hulkenberg	sauber	27	16	16	0	16	53	Finished	5008940	0 days 00:01:21.957000	19	31	0 days 00:01:32.572000
57	2	lawson	rb	30	17	17	0	13	53	Finished	5009717	0 days 00:01:22.734000	17	39	0 days 00:01:32.043000
58	2	ocon	haas	31	18	18	0	18	53	Finished	5010421	0 days 00:01:23.438000	14	48	0 days 00:01:31.967000
59	2	bortoleto	sauber	5	19	19	0	17	53	Finished	5010880	0 days 00:01:23.897000	16	45	0 days 00:01:32.034000
60	2	stroll	aston_martin	18	20	20	0	20	52	Lapped	4939912	0 days 00:00:12.929000	18	52	0 days 00:01:32.052000
61	15	piastri	mclaren	81	1	1	25	1	57	Finished	5739435	0 days 01:35:39.435000	1	36	0 days 00:01:35.140000
62	15	russell	mercedes	63	2	2	18	3	57	Finished	5754934	0 days 00:00:15.499000	2	36	0 days 00:01:35.518000
63	15	norris	mclaren	4	3	3	15	6	57	Finished	5755708	0 days 00:00:16.273000	3	38	0 days 00:01:35.728000
64	15	leclerc	ferrari	16	4	4	12	2	57	Finished	5759114	0 days 00:00:19.679000	4	36	0 days 00:01:36.132000
65	15	hamilton	ferrari	44	5	5	10	9	57	Finished	5767428	0 days 00:00:27.993000	6	37	0 days 00:01:36.235000
66	15	max_verstappen	red_bull	1	6	6	8	7	57	Finished	5773830	0 days 00:00:34.395000	5	29	0 days 00:01:36.167000
67	15	gasly	alpine	10	7	7	6	4	57	Finished	5775437	0 days 00:00:36.002000	7	39	0 days 00:01:36.531000
68	15	ocon	haas	31	8	8	4	14	57	Finished	5783679	0 days 00:00:44.244000	12	30	0 days 00:01:37.098000
69	15	tsunoda	red_bull	22	9	9	2	10	57	Finished	5784496	0 days 00:00:45.061000	14	45	0 days 00:01:37.225000
70	15	bearman	haas	87	10	10	1	20	57	Finished	5787029	0 days 00:00:47.594000	15	40	0 days 00:01:37.303000
71	15	antonelli	mercedes	12	11	11	0	5	57	Finished	5787451	0 days 00:00:48.016000	9	29	0 days 00:01:36.690000
72	15	albon	williams	23	12	12	0	15	57	Finished	5788274	0 days 00:00:48.839000	13	47	0 days 00:01:37.141000
73	15	hadjar	rb	6	13	13	0	12	57	Finished	5795749	0 days 00:00:56.314000	10	30	0 days 00:01:36.952000
74	15	doohan	alpine	7	14	14	0	11	57	Finished	5797241	0 days 00:00:57.806000	8	31	0 days 00:01:36.682000
75	15	alonso	aston_martin	14	15	15	0	13	57	Finished	5799775	0 days 00:01:00.340000	17	38	0 days 00:01:37.906000
76	15	lawson	rb	30	16	16	0	17	57	Finished	5803870	0 days 00:01:04.435000	16	44	0 days 00:01:37.380000
77	15	stroll	aston_martin	18	17	17	0	19	57	Finished	5804924	0 days 00:01:05.489000	19	38	0 days 00:01:38.064000
78	15	bortoleto	sauber	5	18	18	0	18	57	Finished	5806307	0 days 00:01:06.872000	18	38	0 days 00:01:38.006000
79	15	sainz	williams	55	19	R	0	8	45	Retired	\N	\N	11	16	0 days 00:01:36.954000
80	15	hulkenberg	sauber	27	20	D	0	16	0	Disqualified	\N	\N	\N	\N	\N
81	3	piastri	mclaren	81	1	1	25	2	50	Finished	4866758	0 days 01:21:06.758000	3	50	0 days 00:01:32.228000
82	3	max_verstappen	red_bull	1	2	2	18	1	50	Finished	4869601	0 days 00:00:02.843000	4	49	0 days 00:01:32.280000
83	3	leclerc	ferrari	16	3	3	15	4	50	Finished	4874862	0 days 00:00:08.104000	2	49	0 days 00:01:32.192000
84	3	norris	mclaren	4	4	4	12	10	50	Finished	4875954	0 days 00:00:09.196000	1	41	0 days 00:01:31.778000
85	3	russell	mercedes	63	5	5	10	3	50	Finished	4893994	0 days 00:00:27.236000	9	32	0 days 00:01:32.893000
86	3	antonelli	mercedes	12	6	6	8	5	50	Finished	4901446	0 days 00:00:34.688000	5	50	0 days 00:01:32.396000
87	3	hamilton	ferrari	44	7	7	6	7	50	Finished	4905831	0 days 00:00:39.073000	7	43	0 days 00:01:32.600000
88	3	sainz	williams	55	8	8	4	6	50	Finished	4931388	0 days 00:01:04.630000	6	50	0 days 00:01:32.466000
89	3	albon	williams	23	9	9	2	11	50	Finished	4933273	0 days 00:01:06.515000	16	47	0 days 00:01:33.477000
90	3	hadjar	rb	6	10	10	1	14	50	Finished	4933849	0 days 00:01:07.091000	14	39	0 days 00:01:33.257000
91	3	alonso	aston_martin	14	11	11	0	13	50	Finished	4942675	0 days 00:01:15.917000	11	49	0 days 00:01:33.009000
92	3	lawson	rb	30	12	12	0	12	50	Finished	4945209	0 days 00:01:18.451000	10	43	0 days 00:01:32.998000
93	3	bearman	haas	87	13	13	0	15	50	Finished	4945952	0 days 00:01:19.194000	13	50	0 days 00:01:33.238000
94	3	ocon	haas	31	14	14	0	19	50	Finished	4966481	0 days 00:01:39.723000	17	47	0 days 00:01:34.309000
95	3	hulkenberg	sauber	27	15	15	0	18	49	Lapped	4871367	0 days 00:00:04.609000	15	39	0 days 00:01:33.446000
96	3	stroll	aston_martin	18	16	16	0	16	49	Lapped	4872285	0 days 00:00:05.527000	8	44	0 days 00:01:32.745000
97	3	doohan	alpine	7	17	17	0	17	49	Lapped	4886022	0 days 00:00:19.264000	12	48	0 days 00:01:33.150000
98	3	bortoleto	sauber	5	18	18	0	20	49	Lapped	4886064	0 days 00:00:19.306000	18	39	0 days 00:01:34.447000
99	3	tsunoda	red_bull	22	19	R	0	8	1	Retired	\N	\N	\N	\N	\N
100	3	gasly	alpine	10	20	R	0	9	0	Retired	\N	\N	\N	\N	\N
101	4	piastri	mclaren	81	1	1	25	4	57	Finished	5331587	0 days 01:28:51.587000	2	35	0 days 00:01:29.822000
102	4	norris	mclaren	4	2	2	18	2	57	Finished	5336217	0 days 00:00:04.630000	1	36	0 days 00:01:29.746000
103	4	russell	mercedes	63	3	3	15	5	57	Finished	5369231	0 days 00:00:37.644000	3	31	0 days 00:01:30.318000
104	4	max_verstappen	red_bull	1	4	4	12	1	57	Finished	5371543	0 days 00:00:39.956000	5	41	0 days 00:01:30.466000
105	4	albon	williams	23	5	5	10	7	57	Finished	5379654	0 days 00:00:48.067000	6	55	0 days 00:01:30.482000
106	4	antonelli	mercedes	12	6	6	8	3	57	Finished	5387089	0 days 00:00:55.502000	9	27	0 days 00:01:30.795000
107	4	leclerc	ferrari	16	7	7	6	8	57	Finished	5388623	0 days 00:00:57.036000	4	35	0 days 00:01:30.461000
108	4	hamilton	ferrari	44	8	8	4	12	57	Finished	5391773	0 days 00:01:00.186000	7	35	0 days 00:01:30.562000
109	4	sainz	williams	55	9	9	2	6	57	Finished	5392164	0 days 00:01:00.577000	8	35	0 days 00:01:30.703000
110	4	tsunoda	red_bull	22	10	10	1	10	57	Finished	5406021	0 days 00:01:14.434000	10	55	0 days 00:01:30.964000
111	4	hadjar	rb	6	11	11	0	11	57	Finished	5406189	0 days 00:01:14.602000	11	51	0 days 00:01:30.971000
112	4	ocon	haas	31	12	12	0	9	57	Finished	5413593	0 days 00:01:22.006000	13	30	0 days 00:01:31.122000
113	4	gasly	alpine	10	13	13	0	20	57	Finished	5422032	0 days 00:01:30.445000	14	35	0 days 00:01:31.159000
114	4	hulkenberg	sauber	27	14	14	0	16	56	Lapped	5332742	0 days 00:00:01.155000	12	43	0 days 00:01:31.015000
115	4	alonso	aston_martin	14	15	15	0	17	56	Lapped	5352566	0 days 00:00:20.979000	15	38	0 days 00:01:31.287000
116	4	stroll	aston_martin	18	16	16	0	18	56	Lapped	5356749	0 days 00:00:25.162000	16	50	0 days 00:01:31.769000
117	4	lawson	rb	30	17	R	0	15	36	Retired	\N	\N	17	30	0 days 00:01:31.770000
118	4	bortoleto	sauber	5	18	R	0	13	30	Retired	\N	\N	18	21	0 days 00:01:32.328000
119	4	bearman	haas	87	19	R	0	19	27	Retired	\N	\N	19	24	0 days 00:01:32.680000
120	4	doohan	alpine	7	20	R	0	14	0	Retired	\N	\N	\N	\N	\N
121	16	max_verstappen	red_bull	1	1	1	25	2	63	Finished	5493199	0 days 01:31:33.199000	1	58	0 days 00:01:17.988000
122	16	norris	mclaren	4	2	2	18	4	63	Finished	5499308	0 days 00:00:06.109000	4	63	0 days 00:01:18.311000
123	16	piastri	mclaren	81	3	3	15	1	63	Finished	5506155	0 days 00:00:12.956000	5	56	0 days 00:01:18.894000
124	16	hamilton	ferrari	44	4	4	12	12	63	Finished	5507555	0 days 00:00:14.356000	2	61	0 days 00:01:18.265000
125	16	albon	williams	23	5	5	10	7	63	Finished	5511144	0 days 00:00:17.945000	3	63	0 days 00:01:18.289000
126	16	leclerc	ferrari	16	6	6	8	11	63	Finished	5513973	0 days 00:00:20.774000	6	56	0 days 00:01:19.048000
127	16	russell	mercedes	63	7	7	6	3	63	Finished	5515233	0 days 00:00:22.034000	9	55	0 days 00:01:19.733000
128	16	sainz	williams	55	8	8	4	6	63	Finished	5516097	0 days 00:00:22.898000	10	58	0 days 00:01:19.836000
129	16	hadjar	rb	6	9	9	2	9	63	Finished	5516785	0 days 00:00:23.586000	7	60	0 days 00:01:19.473000
130	16	tsunoda	red_bull	22	10	10	1	20	63	Finished	5519645	0 days 00:00:26.446000	12	60	0 days 00:01:20.039000
131	16	alonso	aston_martin	14	11	11	0	5	63	Finished	5520449	0 days 00:00:27.250000	11	61	0 days 00:01:19.894000
132	16	hulkenberg	sauber	27	12	12	0	17	63	Finished	5523495	0 days 00:00:30.296000	15	62	0 days 00:01:20.401000
133	16	gasly	alpine	10	13	13	0	10	63	Finished	5524623	0 days 00:00:31.424000	14	58	0 days 00:01:20.398000
134	16	lawson	rb	30	14	14	0	15	63	Finished	5525710	0 days 00:00:32.511000	16	60	0 days 00:01:20.473000
135	16	stroll	aston_martin	18	15	15	0	8	63	Finished	5526192	0 days 00:00:32.993000	17	58	0 days 00:01:20.501000
136	16	colapinto	alpine	43	16	16	0	16	63	Finished	5526610	0 days 00:00:33.411000	13	57	0 days 00:01:20.345000
137	16	bearman	haas	87	17	17	0	19	63	Finished	5527007	0 days 00:00:33.808000	8	52	0 days 00:01:19.521000
138	16	bortoleto	sauber	5	18	18	0	14	63	Finished	5531771	0 days 00:00:38.572000	19	57	0 days 00:01:20.630000
139	16	antonelli	mercedes	12	19	R	0	13	44	Retired	\N	\N	18	33	0 days 00:01:20.620000
140	16	ocon	haas	31	20	R	0	18	27	Retired	\N	\N	20	3	0 days 00:01:21.413000
141	5	norris	mclaren	4	1	1	25	1	78	Finished	6033843	0 days 01:40:33.843000	1	78	0 days 00:01:13.221000
142	5	leclerc	ferrari	16	2	2	18	2	78	Finished	6036974	0 days 00:00:03.131000	6	36	0 days 00:01:14.055000
143	5	piastri	mclaren	81	3	3	15	3	78	Finished	6037501	0 days 00:00:03.658000	4	60	0 days 00:01:13.745000
144	5	max_verstappen	red_bull	1	4	4	12	4	78	Finished	6054415	0 days 00:00:20.572000	8	45	0 days 00:01:14.230000
145	5	hamilton	ferrari	44	5	5	10	7	78	Finished	6085230	0 days 00:00:51.387000	7	73	0 days 00:01:14.090000
146	5	hadjar	rb	6	6	6	8	5	77	Lapped	6098925	0 days 00:01:05.082000	19	16	0 days 00:01:15.981000
147	5	ocon	haas	31	7	7	6	8	77	Lapped	6099872	0 days 00:01:06.029000	14	34	0 days 00:01:15.157000
148	5	lawson	rb	30	8	8	4	9	77	Lapped	6100589	0 days 00:01:06.746000	17	54	0 days 00:01:15.321000
149	5	albon	williams	23	9	9	2	10	76	Lapped	6045712	0 days 00:00:11.869000	9	74	0 days 00:01:14.597000
150	5	sainz	williams	55	10	10	1	11	76	Lapped	6049075	0 days 00:00:15.232000	5	68	0 days 00:01:13.988000
151	5	russell	mercedes	63	11	11	0	14	76	Lapped	6067687	0 days 00:00:33.844000	2	74	0 days 00:01:13.405000
152	5	bearman	haas	87	12	12	0	20	76	Lapped	6088536	0 days 00:00:54.693000	10	6	0 days 00:01:14.855000
153	5	colapinto	alpine	43	13	13	0	18	76	Lapped	6090957	0 days 00:00:57.114000	16	30	0 days 00:01:15.298000
154	5	bortoleto	sauber	5	14	14	0	16	76	Lapped	6102267	0 days 00:01:08.424000	12	37	0 days 00:01:14.884000
155	5	stroll	aston_martin	18	15	15	0	19	76	Lapped	6104238	0 days 00:01:10.395000	11	67	0 days 00:01:14.877000
156	5	hulkenberg	sauber	27	16	16	0	13	76	Lapped	6105387	0 days 00:01:11.544000	15	47	0 days 00:01:15.223000
157	5	tsunoda	red_bull	22	17	17	0	12	76	Lapped	6105692	0 days 00:01:11.849000	13	75	0 days 00:01:14.913000
158	5	antonelli	mercedes	12	18	18	0	15	75	Lapped	6042252	0 days 00:00:08.409000	3	74	0 days 00:01:13.518000
159	5	alonso	aston_martin	14	19	R	0	6	36	Retired	\N	\N	18	15	0 days 00:01:15.593000
160	5	gasly	alpine	10	20	R	0	17	7	Retired	\N	\N	20	6	0 days 00:01:18.054000
161	6	piastri	mclaren	81	1	1	25	1	66	Finished	5577375	0 days 01:32:57.375000	1	61	0 days 00:01:15.743000
162	6	norris	mclaren	4	2	2	18	2	66	Finished	5579846	0 days 00:00:02.471000	2	61	0 days 00:01:16.187000
163	6	leclerc	ferrari	16	3	3	15	7	66	Finished	5587830	0 days 00:00:10.455000	5	62	0 days 00:01:17.259000
164	6	russell	mercedes	63	4	4	12	4	66	Finished	5588734	0 days 00:00:11.359000	4	62	0 days 00:01:17.244000
165	6	hulkenberg	sauber	27	5	5	10	15	66	Finished	5591023	0 days 00:00:13.648000	6	63	0 days 00:01:17.575000
166	6	hamilton	ferrari	44	6	6	8	5	66	Finished	5592883	0 days 00:00:15.508000	7	62	0 days 00:01:17.706000
167	6	hadjar	rb	6	7	7	6	9	66	Finished	5593397	0 days 00:00:16.022000	8	63	0 days 00:01:17.770000
168	6	gasly	alpine	10	8	8	4	8	66	Finished	5595257	0 days 00:00:17.882000	9	63	0 days 00:01:17.896000
169	6	alonso	aston_martin	14	9	9	2	10	66	Finished	5598939	0 days 00:00:21.564000	11	66	0 days 00:01:18.128000
170	6	max_verstappen	red_bull	1	10	10	1	3	66	Finished	5599201	0 days 00:00:21.826000	3	62	0 days 00:01:17.019000
171	6	lawson	rb	30	11	11	0	13	66	Finished	5602907	0 days 00:00:25.532000	18	62	0 days 00:01:19.424000
172	6	bortoleto	sauber	5	12	12	0	12	66	Finished	5603371	0 days 00:00:25.996000	13	51	0 days 00:01:18.297000
173	6	tsunoda	red_bull	22	13	13	0	19	66	Finished	5606197	0 days 00:00:28.822000	10	46	0 days 00:01:17.998000
174	6	sainz	williams	55	14	14	0	17	66	Finished	5606684	0 days 00:00:29.309000	17	65	0 days 00:01:19.317000
175	6	colapinto	alpine	43	15	15	0	18	66	Finished	5608756	0 days 00:00:31.381000	14	41	0 days 00:01:18.353000
176	6	ocon	haas	31	16	16	0	16	66	Finished	5609572	0 days 00:00:32.197000	15	46	0 days 00:01:18.624000
177	6	bearman	haas	87	17	17	0	14	66	Finished	5614440	0 days 00:00:37.065000	16	63	0 days 00:01:18.907000
178	6	antonelli	mercedes	12	18	R	0	6	53	Retired	\N	\N	12	52	0 days 00:01:18.255000
179	6	albon	williams	23	19	R	0	11	27	Retired	\N	\N	19	9	0 days 00:01:20.508000
180	17	russell	mercedes	63	1	1	25	1	70	Finished	5512688	0 days 01:31:52.688000	1	63	0 days 00:01:14.119000
181	17	max_verstappen	red_bull	1	2	2	18	2	70	Finished	5512916	0 days 00:00:00.228000	5	62	0 days 00:01:14.287000
182	17	antonelli	mercedes	12	3	3	15	4	70	Finished	5513702	0 days 00:00:01.014000	7	60	0 days 00:01:14.455000
183	17	piastri	mclaren	81	4	4	12	3	70	Finished	5514797	0 days 00:00:02.109000	3	64	0 days 00:01:14.255000
184	17	leclerc	ferrari	16	5	5	10	8	70	Finished	5516130	0 days 00:00:03.442000	4	57	0 days 00:01:14.261000
185	17	hamilton	ferrari	44	6	6	8	5	70	Finished	5523401	0 days 00:00:10.713000	9	64	0 days 00:01:14.805000
186	17	alonso	aston_martin	14	7	7	6	6	70	Finished	5523660	0 days 00:00:10.972000	12	58	0 days 00:01:15.024000
187	17	hulkenberg	sauber	27	8	8	4	11	70	Finished	5528052	0 days 00:00:15.364000	14	65	0 days 00:01:15.372000
188	17	ocon	haas	31	9	9	2	14	69	Lapped	5514161	0 days 00:00:01.473000	8	61	0 days 00:01:14.593000
189	17	sainz	williams	55	10	10	1	16	69	Lapped	5514574	0 days 00:00:01.886000	6	59	0 days 00:01:14.389000
190	17	bearman	haas	87	11	11	0	13	69	Lapped	5516405	0 days 00:00:03.717000	15	62	0 days 00:01:15.397000
191	17	tsunoda	red_bull	22	12	12	0	18	69	Lapped	5518144	0 days 00:00:05.456000	13	59	0 days 00:01:15.358000
192	17	colapinto	alpine	43	13	13	0	10	69	Lapped	5519706	0 days 00:00:07.018000	17	53	0 days 00:01:16.076000
193	17	bortoleto	sauber	5	14	14	0	15	69	Lapped	5520567	0 days 00:00:07.879000	16	56	0 days 00:01:15.414000
194	17	gasly	alpine	10	15	15	0	20	69	Lapped	5520638	0 days 00:00:07.950000	11	63	0 days 00:01:14.993000
195	17	hadjar	rb	6	16	16	0	12	69	Lapped	5521425	0 days 00:00:08.737000	19	51	0 days 00:01:16.292000
196	17	stroll	aston_martin	18	17	17	0	17	69	Lapped	5521751	0 days 00:00:09.063000	10	57	0 days 00:01:14.902000
197	17	norris	mclaren	4	18	18	0	7	66	Retired	5042470	\N	2	65	0 days 00:01:14.229000
198	17	lawson	rb	30	19	R	0	19	53	Retired	\N	\N	20	52	0 days 00:01:16.320000
199	17	albon	williams	23	20	R	0	9	46	Retired	\N	\N	18	31	0 days 00:01:16.197000
200	18	norris	mclaren	4	1	1	25	1	70	Finished	5027693	0 days 01:23:47.693000	2	61	0 days 00:01:08.272000
201	18	piastri	mclaren	81	2	2	18	3	70	Finished	5030388	0 days 00:00:02.695000	1	59	0 days 00:01:07.924000
202	18	leclerc	ferrari	16	3	3	15	2	70	Finished	5047513	0 days 00:00:19.820000	4	56	0 days 00:01:08.765000
203	18	hamilton	ferrari	44	4	4	12	4	70	Finished	5056713	0 days 00:00:29.020000	3	53	0 days 00:01:08.628000
204	18	russell	mercedes	63	5	5	10	5	70	Finished	5090089	0 days 00:01:02.396000	7	47	0 days 00:01:09.372000
205	18	lawson	rb	30	6	6	8	6	70	Finished	5095447	0 days 00:01:07.754000	14	58	0 days 00:01:09.977000
206	18	alonso	aston_martin	14	7	7	6	11	69	Lapped	5029130	0 days 00:00:01.437000	12	39	0 days 00:01:09.935000
207	18	bortoleto	sauber	5	8	8	4	8	69	Lapped	5029645	0 days 00:00:01.952000	6	60	0 days 00:01:09.247000
208	18	hulkenberg	sauber	27	9	9	2	20	69	Lapped	5035413	0 days 00:00:07.720000	8	57	0 days 00:01:09.459000
209	18	ocon	haas	31	10	10	1	17	69	Lapped	5037679	0 days 00:00:09.986000	9	55	0 days 00:01:09.550000
210	18	bearman	haas	87	11	11	0	15	69	Lapped	5052547	0 days 00:00:24.854000	13	42	0 days 00:01:09.960000
211	18	hadjar	rb	6	12	12	0	13	69	Lapped	5055650	0 days 00:00:27.957000	16	40	0 days 00:01:10.204000
212	18	gasly	alpine	10	13	13	0	10	69	Lapped	5060748	0 days 00:00:33.055000	15	46	0 days 00:01:10.151000
213	18	stroll	aston_martin	18	14	14	0	16	69	Lapped	5062155	0 days 00:00:34.462000	5	55	0 days 00:01:09.214000
214	18	colapinto	alpine	43	15	15	0	14	69	Lapped	5070385	0 days 00:00:42.692000	10	44	0 days 00:01:09.621000
215	18	tsunoda	red_bull	22	16	16	0	18	68	Lapped	5030672	0 days 00:00:02.979000	11	62	0 days 00:01:09.802000
216	18	albon	williams	23	17	R	0	12	15	Retired	\N	\N	17	9	0 days 00:01:10.641000
217	18	max_verstappen	red_bull	1	18	R	0	7	0	Retired	\N	\N	\N	\N	\N
218	18	antonelli	mercedes	12	19	R	0	9	0	Retired	\N	\N	\N	\N	\N
219	18	sainz	williams	55	20	W	0	19	0	Did not start	\N	\N	\N	\N	\N
220	7	norris	mclaren	4	1	1	25	3	52	Finished	5835735	0 days 01:37:15.735000	2	48	0 days 00:01:29.734000
221	7	piastri	mclaren	81	2	2	18	2	52	Finished	5842547	0 days 00:00:06.812000	1	51	0 days 00:01:29.337000
222	7	hulkenberg	sauber	27	3	3	15	19	52	Finished	5870477	0 days 00:00:34.742000	14	51	0 days 00:01:30.933000
223	7	hamilton	ferrari	44	4	4	12	5	52	Finished	5875547	0 days 00:00:39.812000	3	49	0 days 00:01:30.016000
224	7	max_verstappen	red_bull	1	5	5	10	1	52	Finished	5892516	0 days 00:00:56.781000	5	49	0 days 00:01:30.179000
225	7	gasly	alpine	10	6	6	8	8	52	Finished	5895592	0 days 00:00:59.857000	8	48	0 days 00:01:30.751000
226	7	stroll	aston_martin	18	7	7	6	17	52	Finished	5896338	0 days 00:01:00.603000	15	50	0 days 00:01:32.088000
227	7	albon	williams	23	8	8	4	13	52	Finished	5899870	0 days 00:01:04.135000	4	50	0 days 00:01:30.047000
228	7	alonso	aston_martin	14	9	9	2	7	52	Finished	5901593	0 days 00:01:05.858000	6	49	0 days 00:01:30.353000
229	7	russell	mercedes	63	10	10	1	4	52	Finished	5906409	0 days 00:01:10.674000	11	51	0 days 00:01:30.869000
230	7	bearman	haas	87	11	11	0	18	52	Finished	5907830	0 days 00:01:12.095000	13	50	0 days 00:01:30.921000
231	7	sainz	williams	55	12	12	0	9	52	Finished	5912327	0 days 00:01:16.592000	7	52	0 days 00:01:30.645000
232	7	ocon	haas	31	13	13	0	14	52	Finished	5913036	0 days 00:01:17.301000	9	52	0 days 00:01:30.818000
233	7	leclerc	ferrari	16	14	14	0	6	52	Finished	5920212	0 days 00:01:24.477000	10	50	0 days 00:01:30.819000
234	7	tsunoda	red_bull	22	15	15	0	11	51	Lapped	5867985	0 days 00:00:32.250000	12	49	0 days 00:01:30.873000
235	7	antonelli	mercedes	12	16	R	0	10	23	Retired	\N	\N	17	8	0 days 00:01:45.576000
236	7	hadjar	rb	6	17	R	0	12	17	Retired	\N	\N	16	9	0 days 00:01:41.705000
237	7	bortoleto	sauber	5	18	R	0	16	3	Retired	\N	\N	18	3	0 days 00:02:16.121000
238	7	lawson	rb	30	19	R	0	15	0	Retired	\N	\N	\N	\N	\N
239	7	colapinto	alpine	43	20	W	0	20	0	Did not start	\N	\N	\N	\N	\N
\.


--
-- Data for Name: seasons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.seasons (id, year, name, description, start_date, end_date) FROM stdin;
1	2023	2023 Formula 1 World Championship	第2023赛季F1世界锦标赛	2023-03-01	2023-11-30
2	2024	2024 Formula 1 World Championship	第2024赛季F1世界锦标赛	2024-03-01	2024-11-30
3	2025	2025 Formula 1 World Championship	第2025赛季F1世界锦标赛	2025-03-01	2025-11-30
\.


--
-- Data for Name: sprint_results; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sprint_results (id, race_id, driver_id, constructor_id, number, "position", position_text, points, grid, status, laps, fastest_lap_time, fastest_lap_rank, fastest_lap_number, total_race_time, total_race_time_millis) FROM stdin;
71	1	hamilton	ferrari	44	1	1	8	1	Finished	19	0 days 00:01:35.399000	1	2	0 days 00:30:39.965000	1839965
72	1	piastri	mclaren	81	2	2	7	3	Finished	19	0 days 00:01:35.854000	4	7	0 days 00:00:06.889000	1846854
73	1	max_verstappen	red_bull	1	3	3	6	2	Finished	19	0 days 00:01:35.745000	2	2	0 days 00:00:09.804000	1849769
74	1	russell	mercedes	63	4	4	5	5	Finished	19	0 days 00:01:35.891000	5	4	0 days 00:00:11.592000	1851557
75	1	leclerc	ferrari	16	5	5	4	4	Finished	19	0 days 00:01:36.255000	6	4	0 days 00:00:12.190000	1852155
76	1	tsunoda	rb	22	6	6	3	8	Finished	19	0 days 00:01:36.388000	8	4	0 days 00:00:22.288000	1862253
77	1	antonelli	mercedes	12	7	7	2	7	Finished	19	0 days 00:01:36.311000	7	5	0 days 00:00:23.038000	1863003
78	1	norris	mclaren	4	8	8	1	6	Finished	19	0 days 00:01:36.708000	11	4	0 days 00:00:23.471000	1863436
79	1	stroll	aston_martin	18	9	9	0	10	Finished	19	0 days 00:01:36.435000	9	4	0 days 00:00:24.916000	1864881
80	1	alonso	aston_martin	14	10	10	0	11	Finished	19	0 days 00:01:37.058000	12	8	0 days 00:00:38.218000	1878183
81	1	albon	williams	23	11	11	0	9	Finished	19	0 days 00:01:37.344000	15	7	0 days 00:00:39.292000	1879257
82	1	gasly	alpine	10	12	12	0	17	Finished	19	0 days 00:01:37.481000	17	3	0 days 00:00:39.649000	1879614
83	1	hadjar	rb	6	13	13	0	15	Finished	19	0 days 00:01:37.549000	18	3	0 days 00:00:42.400000	1882365
84	1	lawson	red_bull	30	14	14	0	19	Finished	19	0 days 00:01:37.163000	14	4	0 days 00:00:44.904000	1884869
85	1	bearman	haas	87	15	15	0	12	Finished	19	0 days 00:01:37.135000	13	3	0 days 00:00:45.649000	1885614
86	1	ocon	haas	31	16	16	0	18	Finished	19	0 days 00:01:37.554000	19	3	0 days 00:00:46.182000	1886147
87	1	sainz	williams	55	17	17	0	13	Finished	19	0 days 00:01:35.819000	3	13	0 days 00:00:51.376000	1891341
88	1	bortoleto	sauber	5	18	18	0	14	Finished	19	0 days 00:01:37.475000	16	3	0 days 00:00:53.940000	1893905
89	1	hulkenberg	sauber	27	19	19	0	20	Finished	19	0 days 00:01:36.529000	10	4	0 days 00:00:56.682000	1896647
90	1	doohan	alpine	7	20	20	0	16	Finished	19	0 days 00:01:37.686000	20	3	0 days 00:01:10.212000	1910177
91	4	norris	mclaren	4	1	1	8	3	Finished	18	0 days 00:01:40.334000	5	4	0 days 00:36:37.647000	2197647
92	4	piastri	mclaren	81	2	2	7	2	Finished	18	0 days 00:01:40.238000	4	7	0 days 00:00:00.672000	2198319
93	4	hamilton	ferrari	44	3	3	6	7	Finished	18	0 days 00:01:36.368000	1	13	0 days 00:00:01.073000	2198720
94	4	russell	mercedes	63	4	4	5	5	Finished	18	0 days 00:01:40.963000	7	6	0 days 00:00:03.127000	2200774
95	4	stroll	aston_martin	18	5	5	4	16	Finished	18	0 days 00:01:36.839000	2	13	0 days 00:00:03.412000	2201059
96	4	tsunoda	red_bull	22	6	6	3	20	Finished	18	0 days 00:01:38.078000	3	13	0 days 00:00:05.153000	2202800
97	4	antonelli	mercedes	12	7	7	2	1	Finished	18	0 days 00:01:41.012000	8	6	0 days 00:00:05.635000	2203282
98	4	gasly	alpine	10	8	8	1	13	Finished	18	0 days 00:01:42.694000	16	7	0 days 00:00:05.973000	2203620
99	4	hulkenberg	sauber	27	9	9	0	11	Finished	18	0 days 00:01:42.871000	17	5	0 days 00:00:06.153000	2203800
100	4	hadjar	rb	6	10	10	0	9	Finished	18	0 days 00:01:42.260000	13	6	0 days 00:00:07.502000	2205149
101	4	albon	williams	23	11	11	0	8	Finished	18	0 days 00:01:41.699000	9	7	0 days 00:00:07.522000	2205169
102	4	ocon	haas	31	12	12	0	12	Finished	18	0 days 00:01:42.550000	14	6	0 days 00:00:08.998000	2206645
103	4	lawson	rb	30	13	13	0	14	Finished	18	0 days 00:01:41.922000	11	7	0 days 00:00:09.024000	2206671
104	4	bearman	haas	87	14	14	0	19	Finished	18	0 days 00:01:42.237000	12	5	0 days 00:00:09.218000	2206865
105	4	bortoleto	sauber	5	15	15	0	18	Finished	18	0 days 00:01:42.989000	18	6	0 days 00:00:09.675000	2207322
106	4	doohan	alpine	7	16	16	0	17	Finished	18	0 days 00:01:43.076000	19	7	0 days 00:00:09.909000	2207556
107	4	max_verstappen	red_bull	1	17	17	0	4	Finished	18	0 days 00:01:40.697000	6	5	0 days 00:00:12.059000	2209706
108	4	alonso	aston_martin	14	18	R	0	10	Retired	13	0 days 00:01:41.782000	10	7		\N
109	4	sainz	williams	55	19	R	0	15	Retired	12	0 days 00:01:42.638000	15	5		\N
110	4	leclerc	ferrari	16	20	R	0	6	Retired	0		\N	\N		\N
\.


--
-- Name: constructor_standings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.constructor_standings_id_seq', 100, true);


--
-- Name: driver_seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.driver_seasons_id_seq', 42, true);


--
-- Name: driver_standings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.driver_standings_id_seq', 192, true);


--
-- Name: qualifying_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.qualifying_results_id_seq', 440, true);


--
-- Name: races_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.races_id_seq', 25, true);


--
-- Name: results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.results_id_seq', 239, true);


--
-- Name: seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.seasons_id_seq', 3, true);


--
-- Name: sprint_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sprint_results_id_seq', 110, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: circuits circuits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.circuits
    ADD CONSTRAINT circuits_pkey PRIMARY KEY (circuit_id);


--
-- Name: constructor_standings constructor_standings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructor_standings
    ADD CONSTRAINT constructor_standings_pkey PRIMARY KEY (id);


--
-- Name: constructors constructors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructors
    ADD CONSTRAINT constructors_pkey PRIMARY KEY (constructor_id);


--
-- Name: driver_seasons driver_seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_seasons
    ADD CONSTRAINT driver_seasons_pkey PRIMARY KEY (id);


--
-- Name: driver_standings driver_standings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_standings
    ADD CONSTRAINT driver_standings_pkey PRIMARY KEY (id);


--
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (driver_id);


--
-- Name: qualifying_results qualifying_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualifying_results
    ADD CONSTRAINT qualifying_results_pkey PRIMARY KEY (id);


--
-- Name: races races_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.races
    ADD CONSTRAINT races_pkey PRIMARY KEY (id);


--
-- Name: results results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_pkey PRIMARY KEY (id);


--
-- Name: seasons seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seasons
    ADD CONSTRAINT seasons_pkey PRIMARY KEY (id);


--
-- Name: sprint_results sprint_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sprint_results
    ADD CONSTRAINT sprint_results_pkey PRIMARY KEY (id);


--
-- Name: idx_constructor_standing_season; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_constructor_standing_season ON public.constructor_standings USING btree (season_id);


--
-- Name: idx_constructor_standing_season_constructor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_constructor_standing_season_constructor ON public.constructor_standings USING btree (season_id, constructor_id);


--
-- Name: idx_driver_standing_season; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_driver_standing_season ON public.driver_standings USING btree (season_id);


--
-- Name: idx_driver_standing_season_constructor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_driver_standing_season_constructor ON public.driver_standings USING btree (season_id, constructor_id);


--
-- Name: idx_driver_standing_season_driver; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_driver_standing_season_driver ON public.driver_standings USING btree (season_id, driver_id);


--
-- Name: ix_circuits_circuit_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_circuits_circuit_id ON public.circuits USING btree (circuit_id);


--
-- Name: ix_constructor_standings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_constructor_standings_id ON public.constructor_standings USING btree (id);


--
-- Name: ix_constructors_constructor_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_constructors_constructor_id ON public.constructors USING btree (constructor_id);


--
-- Name: ix_driver_seasons_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_driver_seasons_id ON public.driver_seasons USING btree (id);


--
-- Name: ix_driver_standings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_driver_standings_id ON public.driver_standings USING btree (id);


--
-- Name: ix_drivers_driver_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_drivers_driver_id ON public.drivers USING btree (driver_id);


--
-- Name: ix_qualifying_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_qualifying_results_id ON public.qualifying_results USING btree (id);


--
-- Name: ix_races_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_races_id ON public.races USING btree (id);


--
-- Name: ix_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_results_id ON public.results USING btree (id);


--
-- Name: ix_seasons_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_seasons_id ON public.seasons USING btree (id);


--
-- Name: ix_seasons_year; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_seasons_year ON public.seasons USING btree (year);


--
-- Name: ix_sprint_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sprint_results_id ON public.sprint_results USING btree (id);


--
-- Name: constructor_standings constructor_standings_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructor_standings
    ADD CONSTRAINT constructor_standings_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: constructor_standings constructor_standings_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructor_standings
    ADD CONSTRAINT constructor_standings_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(id);


--
-- Name: constructors constructors_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constructors
    ADD CONSTRAINT constructors_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(id);


--
-- Name: driver_seasons driver_seasons_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_seasons
    ADD CONSTRAINT driver_seasons_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: driver_seasons driver_seasons_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_seasons
    ADD CONSTRAINT driver_seasons_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: driver_seasons driver_seasons_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_seasons
    ADD CONSTRAINT driver_seasons_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(id);


--
-- Name: driver_standings driver_standings_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_standings
    ADD CONSTRAINT driver_standings_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: driver_standings driver_standings_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_standings
    ADD CONSTRAINT driver_standings_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: driver_standings driver_standings_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_standings
    ADD CONSTRAINT driver_standings_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(id);


--
-- Name: qualifying_results qualifying_results_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualifying_results
    ADD CONSTRAINT qualifying_results_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: qualifying_results qualifying_results_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualifying_results
    ADD CONSTRAINT qualifying_results_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: qualifying_results qualifying_results_race_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualifying_results
    ADD CONSTRAINT qualifying_results_race_id_fkey FOREIGN KEY (race_id) REFERENCES public.races(id);


--
-- Name: races races_circuit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.races
    ADD CONSTRAINT races_circuit_id_fkey FOREIGN KEY (circuit_id) REFERENCES public.circuits(circuit_id);


--
-- Name: races races_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.races
    ADD CONSTRAINT races_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(id);


--
-- Name: results results_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: results results_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: results results_race_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_race_id_fkey FOREIGN KEY (race_id) REFERENCES public.races(id);


--
-- Name: sprint_results sprint_results_constructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sprint_results
    ADD CONSTRAINT sprint_results_constructor_id_fkey FOREIGN KEY (constructor_id) REFERENCES public.constructors(constructor_id);


--
-- Name: sprint_results sprint_results_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sprint_results
    ADD CONSTRAINT sprint_results_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: sprint_results sprint_results_race_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sprint_results
    ADD CONSTRAINT sprint_results_race_id_fkey FOREIGN KEY (race_id) REFERENCES public.races(id);


--
-- PostgreSQL database dump complete
--

