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

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.alembic_version VALUES ('f17a20b245aa');


--
-- Data for Name: circuits; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.circuits VALUES ('hungaroring', 'https://en.wikipedia.org/wiki/Hungaroring', 'Hungaroring', 47.5789, 19.2486, 'Budapest', 'Hungary', 4381, NULL, '1:16.627', 'Lewis Hamilton', 2020, NULL, NULL, true, 1986, 70, 306.63, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.webp', 'static/circuit_images/hungaroring_circuit.webp');
INSERT INTO public.circuits VALUES ('red_bull_ring', 'https://en.wikipedia.org/wiki/Red_Bull_Ring', 'Red Bull Ring', 47.2197, 14.7647, 'Spielberg', 'Austria', 4326, NULL, '1:07.924', 'Oscar Piastri', 2025, NULL, NULL, true, 1970, 71, 307.018, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.webp', 'static/circuit_images/red_bull_ring_circuit.webp');
INSERT INTO public.circuits VALUES ('rodriguez', 'https://en.wikipedia.org/wiki/Aut%C3%B3dromo_Hermanos_Rodr%C3%ADguez', 'Autódromo Hermanos Rodríguez', 19.4042, -99.0907, 'Mexico City', 'Mexico', 4304, NULL, '1:17.774', 'Valtteri Bottas', 2021, NULL, NULL, true, 1963, 71, 305.354, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.webp', 'static/circuit_images/rodriguez_circuit.webp');
INSERT INTO public.circuits VALUES ('yas_marina', 'https://en.wikipedia.org/wiki/Yas_Marina_Circuit', 'Yas Marina Circuit', 24.4672, 54.6031, 'Abu Dhabi', 'UAE', 5281, NULL, '1:25.637', 'Kevin Magnussen', 2024, NULL, NULL, false, 2009, 58, 306.183, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.webp', 'static/circuit_images/yas_marina_circuit.webp');
INSERT INTO public.circuits VALUES ('shanghai', 'https://en.wikipedia.org/wiki/Shanghai_International_Circuit', 'Shanghai International Circuit', 31.3389, 121.22, 'Shanghai', 'China', 5451, NULL, '1:32.238', 'Michael Schumacher', 2004, NULL, NULL, true, 2004, 56, 305.066, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.webp', 'static/circuit_images/shanghai_circuit.webp');
INSERT INTO public.circuits VALUES ('suzuka', 'https://en.wikipedia.org/wiki/Suzuka_International_Racing_Course', 'Suzuka Circuit', 34.8431, 136.541, 'Suzuka', 'Japan', 5807, NULL, '1:30.965', 'Kimi Antonelli', 2025, NULL, NULL, true, 1987, 53, 307.471, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.webp', 'static/circuit_images/suzuka_circuit.webp');
INSERT INTO public.circuits VALUES ('zandvoort', 'https://en.wikipedia.org/wiki/Circuit_Zandvoort', 'Circuit Park Zandvoort', 52.3888, 4.54092, 'Zandvoort', 'Netherlands', 4259, NULL, '1:11.097', 'Lewis Hamilton', 2021, NULL, NULL, true, 1952, 72, 306.587, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.webp', 'static/circuit_images/zandvoort_circuit.webp');
INSERT INTO public.circuits VALUES ('baku', 'https://en.wikipedia.org/wiki/Baku_City_Circuit', 'Baku City Circuit', 40.3725, 49.8533, 'Baku', 'Azerbaijan', 6003, NULL, '1:43.009', 'Charles Leclerc', 2019, NULL, NULL, true, 2016, 51, 306.049, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.webp', 'static/circuit_images/Baku_Circuit.webp');
INSERT INTO public.circuits VALUES ('catalunya', 'https://en.wikipedia.org/wiki/Circuit_de_Barcelona-Catalunya', 'Circuit de Barcelona-Catalunya', 41.57, 2.26111, 'Montmeló', 'Spain', 4657, NULL, '1:15.743', 'Oscar Piastri', 2025, NULL, NULL, false, 1991, 66, 307.236, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.webp', 'static/circuit_images/catalunya_circuit.webp');
INSERT INTO public.circuits VALUES ('monaco', 'https://en.wikipedia.org/wiki/Circuit_de_Monaco', 'Circuit de Monaco', 43.7347, 7.42056, 'Monte-Carlo', 'Monaco', 3337, NULL, '1:12.909', 'Lewis Hamilton', 2021, NULL, NULL, false, 1950, 78, 260.286, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.webp', 'static/circuit_images/monaco_circuit.webp');
INSERT INTO public.circuits VALUES ('vegas', 'https://en.wikipedia.org/wiki/Las_Vegas_Grand_Prix#Circuit', 'Las Vegas Strip Street Circuit', 36.1147, -115.173, 'Las Vegas', 'USA', 6201, NULL, '1:34.876', 'Lando Norris', 2024, NULL, NULL, false, 2023, 50, 309.958, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.webp', 'static/circuit_images/vegas_circuit.webp');
INSERT INTO public.circuits VALUES ('albert_park', 'https://en.wikipedia.org/wiki/Albert_Park_Circuit', 'Albert Park Grand Prix Circuit', -37.8497, 144.968, 'Melbourne', 'Australia', 5278, NULL, '1:19.813', 'Charles Leclerc', 2024, NULL, NULL, true, 1996, 58, 306.124, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.webp', 'static/circuit_images/albert_park_circuit.webp');
INSERT INTO public.circuits VALUES ('bahrain', 'https://en.wikipedia.org/wiki/Bahrain_International_Circuit', 'Bahrain International Circuit', 26.0325, 50.5106, 'Sakhir', 'Bahrain', 5412, NULL, '1:31.447', 'Pedro de la Rosa', 2005, NULL, NULL, true, 2004, 57, 308.238, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.webp', 'static/circuit_images/bahrain_circuit.webp');
INSERT INTO public.circuits VALUES ('interlagos', 'https://en.wikipedia.org/wiki/Interlagos_Circuit', 'Autódromo José Carlos Pace', -23.7036, -46.6997, 'São Paulo', 'Brazil', 4309, NULL, '1:10.540', 'Valtteri Bottas', 2018, NULL, NULL, true, 1973, 71, 305.879, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.webp', 'static/circuit_images/interlagos_circuit.webp');
INSERT INTO public.circuits VALUES ('jeddah', 'https://en.wikipedia.org/wiki/Jeddah_Corniche_Circuit', 'Jeddah Corniche Circuit', 21.6319, 39.1044, 'Jeddah', 'Saudi Arabia', 6174, NULL, '1:30.734', 'Lewis Hamilton', 2021, NULL, NULL, true, 2021, 50, 308.45, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.webp', 'static/circuit_images/jeddah_circuit.webp');
INSERT INTO public.circuits VALUES ('marina_bay', 'https://en.wikipedia.org/wiki/Marina_Bay_Street_Circuit', 'Marina Bay Street Circuit', 1.2914, 103.864, 'Marina Bay', 'Singapore', 4940, NULL, '1:34.486', 'Daniel Ricciardo', 2024, NULL, NULL, true, 2008, 62, 306.143, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.webp', 'static/circuit_images/marina_bay_circuit.webp');
INSERT INTO public.circuits VALUES ('monza', 'https://en.wikipedia.org/wiki/Monza_Circuit', 'Autodromo Nazionale di Monza', 45.6156, 9.28111, 'Monza', 'Italy', 5793, NULL, '1:21.046', 'Rubens Barrichello', 2004, NULL, NULL, true, 1950, 53, 306.72, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.webp', 'static/circuit_images/monza_circuit.webp');
INSERT INTO public.circuits VALUES ('spa', 'https://en.wikipedia.org/wiki/Circuit_de_Spa-Francorchamps', 'Circuit de Spa-Francorchamps', 50.4372, 5.97139, 'Spa', 'Belgium', 7004, NULL, '1:44.701', 'Sergio Perez', 2024, NULL, NULL, false, 1950, 44, 308.052, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.webp', 'static/circuit_images/spa_circuit.webp');
INSERT INTO public.circuits VALUES ('losail', 'https://en.wikipedia.org/wiki/Lusail_International_Circuit', 'Losail International Circuit', 25.49, 51.4542, 'Al Daayen', 'Qatar', 5419, NULL, '1:22.384', 'Lando Norris', 2024, NULL, NULL, false, 2021, 57, 308.611, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Qatar_Circuit.webp', 'static/circuit_images/losail_circuit.webp');
INSERT INTO public.circuits VALUES ('miami', 'https://en.wikipedia.org/wiki/Miami_International_Autodrome', 'Miami International Autodrome', 25.9581, -80.2389, 'Miami', 'USA', 5412, NULL, '1:29.708', 'Max Verstappen', 2023, NULL, NULL, false, 2022, 57, 308.326, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.webp', 'static/circuit_images/miami_circuit.webp');
INSERT INTO public.circuits VALUES ('silverstone', 'https://en.wikipedia.org/wiki/Silverstone_Circuit', 'Silverstone Circuit', 52.0786, -1.01694, 'Silverstone', 'UK', 5891, NULL, '1:27.097', 'Max Verstappen', 2020, NULL, NULL, false, 1950, 52, 306.198, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.webp', 'static/circuit_images/silverstone_circuit.webp');
INSERT INTO public.circuits VALUES ('villeneuve', 'https://en.wikipedia.org/wiki/Circuit_Gilles_Villeneuve', 'Circuit Gilles Villeneuve', 45.5, -73.5228, 'Montreal', 'Canada', 4361, NULL, '1:13.078', 'Valtteri Bottas', 2019, NULL, NULL, false, 1978, 70, 305.27, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.webp', 'static/circuit_images/villeneuve_circuit.webp');
INSERT INTO public.circuits VALUES ('imola', 'https://en.wikipedia.org/wiki/Imola_Circuit', 'Autodromo Enzo e Dino Ferrari', 44.3439, 11.7167, 'Imola', 'Italy', 4909, NULL, '1:15.484', 'Lewis Hamilton', 2020, NULL, NULL, true, 1980, 63, 309.049, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Emilia_Romagna_Circuit.webp', 'static/circuit_images/imola_circuit.webp');
INSERT INTO public.circuits VALUES ('americas', 'https://en.wikipedia.org/wiki/Circuit_of_the_Americas', 'Circuit of the Americas', 30.1328, -97.6411, 'Austin', 'USA', 5513, NULL, '1:36.169', 'Charles Leclerc', 2019, NULL, NULL, false, 2012, 56, 308.405, 'https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.webp', 'static/circuit_images/USA_Circuit.webp');


--
-- Data for Name: seasons; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.seasons VALUES (1, 2023, '2023 Formula 1 World Championship', '第2023赛季F1世界锦标赛', '2023-03-01', '2023-11-30');
INSERT INTO public.seasons VALUES (2, 2024, '2024 Formula 1 World Championship', '第2024赛季F1世界锦标赛', '2024-03-01', '2024-11-30');
INSERT INTO public.seasons VALUES (3, 2025, '2025 Formula 1 World Championship', '第2025赛季F1世界锦标赛', '2025-03-01', '2025-11-30');


--
-- Data for Name: constructors; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.constructors VALUES ('alpine', 'http://en.wikipedia.org/wiki/Alpine_F1_Team', 'Alpine F1 Team', 'French', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('aston_martin', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'Aston Martin', 'British', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('ferrari', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'Ferrari', 'Italian', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('haas', 'http://en.wikipedia.org/wiki/Haas_F1_Team', 'Haas F1 Team', 'American', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('mclaren', 'http://en.wikipedia.org/wiki/McLaren', 'McLaren', 'British', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('mercedes', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'Mercedes', 'German', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('rb', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'RB F1 Team', 'Italian', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('red_bull', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'Red Bull', 'Austrian', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('sauber', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'Sauber', 'Swiss', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);
INSERT INTO public.constructors VALUES ('williams', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'Williams', 'British', 3, NULL, NULL, NULL, NULL, true, 0, 0, 0, 0, 0);


--
-- Data for Name: constructor_standings; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.constructor_standings VALUES (121, 3, 'mclaren', 1, 623, 12, '1');
INSERT INTO public.constructor_standings VALUES (122, 3, 'mercedes', 2, 290, 1, '2');
INSERT INTO public.constructor_standings VALUES (123, 3, 'ferrari', 3, 286, 0, '3');
INSERT INTO public.constructor_standings VALUES (124, 3, 'red_bull', 4, 272, 4, '4');
INSERT INTO public.constructor_standings VALUES (125, 3, 'williams', 5, 101, 0, '5');
INSERT INTO public.constructor_standings VALUES (126, 3, 'rb', 6, 72, 0, '6');
INSERT INTO public.constructor_standings VALUES (127, 3, 'aston_martin', 7, 62, 0, '7');
INSERT INTO public.constructor_standings VALUES (128, 3, 'sauber', 8, 55, 0, '8');
INSERT INTO public.constructor_standings VALUES (129, 3, 'haas', 9, 44, 0, '9');
INSERT INTO public.constructor_standings VALUES (130, 3, 'alpine', 10, 20, 0, '10');
INSERT INTO public.constructor_standings VALUES (51, 2, 'mclaren', 1, 666, 6, '1');
INSERT INTO public.constructor_standings VALUES (52, 2, 'ferrari', 2, 652, 5, '2');
INSERT INTO public.constructor_standings VALUES (53, 2, 'red_bull', 3, 589, 9, '3');
INSERT INTO public.constructor_standings VALUES (54, 2, 'mercedes', 4, 468, 4, '4');
INSERT INTO public.constructor_standings VALUES (55, 2, 'aston_martin', 5, 94, 0, '5');
INSERT INTO public.constructor_standings VALUES (56, 2, 'alpine', 6, 65, 0, '6');
INSERT INTO public.constructor_standings VALUES (57, 2, 'haas', 7, 58, 0, '7');
INSERT INTO public.constructor_standings VALUES (58, 2, 'rb', 8, 46, 0, '8');
INSERT INTO public.constructor_standings VALUES (59, 2, 'williams', 9, 17, 0, '9');
INSERT INTO public.constructor_standings VALUES (60, 2, 'sauber', 10, 4, 0, '10');


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.drivers VALUES ('albon', 23, 'ALB', 'http://en.wikipedia.org/wiki/Alexander_Albon', 'Alexander', 'Albon', '1996-03-23', 'Thai');
INSERT INTO public.drivers VALUES ('alonso', 14, 'ALO', 'http://en.wikipedia.org/wiki/Fernando_Alonso', 'Fernando', 'Alonso', '1981-07-29', 'Spanish');
INSERT INTO public.drivers VALUES ('antonelli', 12, 'ANT', 'https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli', 'Andrea Kimi', 'Antonelli', '2006-08-25', 'Italian');
INSERT INTO public.drivers VALUES ('bearman', 87, 'BEA', 'http://en.wikipedia.org/wiki/Oliver_Bearman', 'Oliver', 'Bearman', '2005-05-08', 'British');
INSERT INTO public.drivers VALUES ('bortoleto', 5, 'BOR', 'https://en.wikipedia.org/wiki/Gabriel_Bortoleto', 'Gabriel', 'Bortoleto', '2004-10-14', 'Brazilian');
INSERT INTO public.drivers VALUES ('colapinto', 43, 'COL', 'http://en.wikipedia.org/wiki/Franco_Colapinto', 'Franco', 'Colapinto', '2003-05-27', 'Argentine');
INSERT INTO public.drivers VALUES ('doohan', 7, 'DOO', 'http://en.wikipedia.org/wiki/Jack_Doohan', 'Jack', 'Doohan', '2003-01-20', 'Australian');
INSERT INTO public.drivers VALUES ('gasly', 10, 'GAS', 'http://en.wikipedia.org/wiki/Pierre_Gasly', 'Pierre', 'Gasly', '1996-02-07', 'French');
INSERT INTO public.drivers VALUES ('hadjar', 6, 'HAD', 'https://en.wikipedia.org/wiki/Isack_Hadjar', 'Isack', 'Hadjar', '2004-09-28', 'French');
INSERT INTO public.drivers VALUES ('hamilton', 44, 'HAM', 'http://en.wikipedia.org/wiki/Lewis_Hamilton', 'Lewis', 'Hamilton', '1985-01-07', 'British');
INSERT INTO public.drivers VALUES ('hulkenberg', 27, 'HUL', 'http://en.wikipedia.org/wiki/Nico_H%C3%BClkenberg', 'Nico', 'Hülkenberg', '1987-08-19', 'German');
INSERT INTO public.drivers VALUES ('lawson', 30, 'LAW', 'http://en.wikipedia.org/wiki/Liam_Lawson', 'Liam', 'Lawson', '2002-02-11', 'New Zealander');
INSERT INTO public.drivers VALUES ('leclerc', 16, 'LEC', 'http://en.wikipedia.org/wiki/Charles_Leclerc', 'Charles', 'Leclerc', '1997-10-16', 'Monegasque');
INSERT INTO public.drivers VALUES ('norris', 4, 'NOR', 'http://en.wikipedia.org/wiki/Lando_Norris', 'Lando', 'Norris', '1999-11-13', 'British');
INSERT INTO public.drivers VALUES ('ocon', 31, 'OCO', 'http://en.wikipedia.org/wiki/Esteban_Ocon', 'Esteban', 'Ocon', '1996-09-17', 'French');
INSERT INTO public.drivers VALUES ('piastri', 81, 'PIA', 'http://en.wikipedia.org/wiki/Oscar_Piastri', 'Oscar', 'Piastri', '2001-04-06', 'Australian');
INSERT INTO public.drivers VALUES ('russell', 63, 'RUS', 'http://en.wikipedia.org/wiki/George_Russell_(racing_driver)', 'George', 'Russell', '1998-02-15', 'British');
INSERT INTO public.drivers VALUES ('sainz', 55, 'SAI', 'http://en.wikipedia.org/wiki/Carlos_Sainz_Jr.', 'Carlos', 'Sainz', '1994-09-01', 'Spanish');
INSERT INTO public.drivers VALUES ('stroll', 18, 'STR', 'http://en.wikipedia.org/wiki/Lance_Stroll', 'Lance', 'Stroll', '1998-10-29', 'Canadian');
INSERT INTO public.drivers VALUES ('tsunoda', 22, 'TSU', 'http://en.wikipedia.org/wiki/Yuki_Tsunoda', 'Yuki', 'Tsunoda', '2000-05-11', 'Japanese');
INSERT INTO public.drivers VALUES ('max_verstappen', 33, 'VER', 'http://en.wikipedia.org/wiki/Max_Verstappen', 'Max', 'Verstappen', '1997-09-30', 'Dutch');
INSERT INTO public.drivers VALUES ('perez', 11, 'PER', 'http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez', 'Sergio', 'Pérez', '1990-01-26', 'Mexican');
INSERT INTO public.drivers VALUES ('kevin_magnussen', 20, 'MAG', 'http://en.wikipedia.org/wiki/Kevin_Magnussen', 'Kevin', 'Magnussen', '1992-10-05', 'Danish');
INSERT INTO public.drivers VALUES ('ricciardo', 3, 'RIC', 'http://en.wikipedia.org/wiki/Daniel_Ricciardo', 'Daniel', 'Ricciardo', '1989-07-01', 'Australian');
INSERT INTO public.drivers VALUES ('zhou', 24, 'ZHO', 'http://en.wikipedia.org/wiki/Zhou_Guanyu', 'Guanyu', 'Zhou', '1999-05-30', 'Chinese');
INSERT INTO public.drivers VALUES ('bottas', 77, 'BOT', 'http://en.wikipedia.org/wiki/Valtteri_Bottas', 'Valtteri', 'Bottas', '1989-08-28', 'Finnish');
INSERT INTO public.drivers VALUES ('sargeant', 2, 'SAR', 'http://en.wikipedia.org/wiki/Logan_Sargeant', 'Logan', 'Sargeant', '2000-12-31', 'American');


--
-- Data for Name: driver_seasons; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.driver_seasons VALUES (41, 'lawson', 'rb', 3);
INSERT INTO public.driver_seasons VALUES (42, 'tsunoda', 'red_bull', 3);


--
-- Data for Name: driver_standings; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.driver_standings VALUES (85, 2, 'max_verstappen', 'red_bull', 1, 437, 9, '1');
INSERT INTO public.driver_standings VALUES (86, 2, 'norris', 'mclaren', 2, 374, 4, '2');
INSERT INTO public.driver_standings VALUES (87, 2, 'leclerc', 'ferrari', 3, 356, 3, '3');
INSERT INTO public.driver_standings VALUES (88, 2, 'piastri', 'mclaren', 4, 292, 2, '4');
INSERT INTO public.driver_standings VALUES (89, 2, 'sainz', 'ferrari', 5, 290, 2, '5');
INSERT INTO public.driver_standings VALUES (90, 2, 'russell', 'mercedes', 6, 245, 2, '6');
INSERT INTO public.driver_standings VALUES (91, 2, 'hamilton', 'mercedes', 7, 223, 2, '7');
INSERT INTO public.driver_standings VALUES (92, 2, 'perez', 'red_bull', 8, 152, 0, '8');
INSERT INTO public.driver_standings VALUES (93, 2, 'alonso', 'aston_martin', 9, 70, 0, '9');
INSERT INTO public.driver_standings VALUES (94, 2, 'gasly', 'alpine', 10, 42, 0, '10');
INSERT INTO public.driver_standings VALUES (95, 2, 'hulkenberg', 'haas', 11, 41, 0, '11');
INSERT INTO public.driver_standings VALUES (96, 2, 'tsunoda', 'rb', 12, 30, 0, '12');
INSERT INTO public.driver_standings VALUES (97, 2, 'stroll', 'aston_martin', 13, 24, 0, '13');
INSERT INTO public.driver_standings VALUES (98, 2, 'ocon', 'alpine', 14, 23, 0, '14');
INSERT INTO public.driver_standings VALUES (99, 2, 'kevin_magnussen', 'haas', 15, 16, 0, '15');
INSERT INTO public.driver_standings VALUES (100, 2, 'albon', 'williams', 16, 12, 0, '16');
INSERT INTO public.driver_standings VALUES (101, 2, 'ricciardo', 'rb', 17, 12, 0, '17');
INSERT INTO public.driver_standings VALUES (102, 2, 'bearman', 'ferrari', 18, 7, 0, '18');
INSERT INTO public.driver_standings VALUES (103, 2, 'colapinto', 'williams', 19, 5, 0, '19');
INSERT INTO public.driver_standings VALUES (104, 2, 'zhou', 'sauber', 20, 4, 0, '20');
INSERT INTO public.driver_standings VALUES (105, 2, 'lawson', 'rb', 21, 4, 0, '21');
INSERT INTO public.driver_standings VALUES (106, 2, 'bottas', 'sauber', 22, 0, 0, '22');
INSERT INTO public.driver_standings VALUES (107, 2, 'sargeant', 'williams', 23, 0, 0, '23');
INSERT INTO public.driver_standings VALUES (108, 2, 'doohan', 'alpine', 24, 0, 0, '24');
INSERT INTO public.driver_standings VALUES (235, 3, 'piastri', 'mclaren', 1, 324, 7, '1');
INSERT INTO public.driver_standings VALUES (236, 3, 'norris', 'mclaren', 2, 299, 5, '2');
INSERT INTO public.driver_standings VALUES (237, 3, 'max_verstappen', 'red_bull', 3, 255, 4, '3');
INSERT INTO public.driver_standings VALUES (238, 3, 'russell', 'mercedes', 4, 212, 1, '4');
INSERT INTO public.driver_standings VALUES (239, 3, 'leclerc', 'ferrari', 5, 165, 0, '5');
INSERT INTO public.driver_standings VALUES (240, 3, 'hamilton', 'ferrari', 6, 121, 0, '6');
INSERT INTO public.driver_standings VALUES (241, 3, 'antonelli', 'mercedes', 7, 78, 0, '7');
INSERT INTO public.driver_standings VALUES (242, 3, 'albon', 'williams', 8, 70, 0, '8');
INSERT INTO public.driver_standings VALUES (243, 3, 'hadjar', 'rb', 9, 39, 0, '9');
INSERT INTO public.driver_standings VALUES (244, 3, 'hulkenberg', 'sauber', 10, 37, 0, '10');
INSERT INTO public.driver_standings VALUES (245, 3, 'stroll', 'aston_martin', 11, 32, 0, '11');
INSERT INTO public.driver_standings VALUES (246, 3, 'sainz', 'williams', 12, 31, 0, '12');
INSERT INTO public.driver_standings VALUES (247, 3, 'lawson', 'red_bull', 13, 30, 0, '13');
INSERT INTO public.driver_standings VALUES (248, 3, 'alonso', 'aston_martin', 14, 30, 0, '14');
INSERT INTO public.driver_standings VALUES (249, 3, 'ocon', 'haas', 15, 28, 0, '15');
INSERT INTO public.driver_standings VALUES (250, 3, 'gasly', 'alpine', 16, 20, 0, '16');
INSERT INTO public.driver_standings VALUES (251, 3, 'tsunoda', 'rb', 17, 20, 0, '17');
INSERT INTO public.driver_standings VALUES (252, 3, 'bortoleto', 'sauber', 18, 18, 0, '18');
INSERT INTO public.driver_standings VALUES (253, 3, 'bearman', 'haas', 19, 16, 0, '19');
INSERT INTO public.driver_standings VALUES (254, 3, 'colapinto', 'alpine', 20, 0, 0, '20');
INSERT INTO public.driver_standings VALUES (255, 3, 'doohan', 'alpine', 21, 0, 0, '21');


--
-- Data for Name: races; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.races VALUES (4, 3, 'miami', 6, 'United States', 'Miami', 'Miami Grand Prix', '2025-05-04', 'sprint_qualifying', 'Practice 1', '2025-05-02 16:30:00', 'Sprint Qualifying', '2025-05-02 20:30:00', 'Sprint', '2025-05-03 16:00:00', 'Qualifying', '2025-05-03 20:00:00', 'Race', '2025-05-04 20:00:00', true);
INSERT INTO public.races VALUES (5, 3, 'monaco', 8, 'Monaco', 'Monaco', 'Monaco Grand Prix', '2025-05-25', 'conventional', 'Practice 1', '2025-05-23 11:30:00', 'Practice 2', '2025-05-23 15:00:00', 'Practice 3', '2025-05-24 10:30:00', 'Qualifying', '2025-05-24 14:00:00', 'Race', '2025-05-25 13:00:00', false);
INSERT INTO public.races VALUES (6, 3, 'catalunya', 9, 'Spain', 'Barcelona', 'Spanish Grand Prix', '2025-06-01', 'conventional', 'Practice 1', '2025-05-30 11:30:00', 'Practice 2', '2025-05-30 15:00:00', 'Practice 3', '2025-05-31 10:30:00', 'Qualifying', '2025-05-31 14:00:00', 'Race', '2025-06-01 13:00:00', false);
INSERT INTO public.races VALUES (7, 3, 'silverstone', 12, 'United Kingdom', 'Silverstone', 'British Grand Prix', '2025-07-06', 'conventional', 'Practice 1', '2025-07-04 11:30:00', 'Practice 2', '2025-07-04 15:00:00', 'Practice 3', '2025-07-05 10:30:00', 'Qualifying', '2025-07-05 14:00:00', 'Race', '2025-07-06 14:00:00', false);
INSERT INTO public.races VALUES (8, 3, 'spa', 13, 'Belgium', 'Spa-Francorchamps', 'Belgian Grand Prix', '2025-07-27', 'sprint_qualifying', 'Practice 1', '2025-07-25 10:30:00', 'Sprint Qualifying', '2025-07-25 14:30:00', 'Sprint', '2025-07-26 10:00:00', 'Qualifying', '2025-07-26 14:00:00', 'Race', '2025-07-27 13:00:00', true);
INSERT INTO public.races VALUES (1, 3, 'shanghai', 2, 'China', 'Shanghai', 'Chinese Grand Prix', '2025-03-23', 'sprint_qualifying', 'Practice 1', '2025-03-21 03:30:00', 'Sprint Qualifying', '2025-03-21 07:30:00', 'Sprint', '2025-03-22 03:00:00', 'Qualifying', '2025-03-22 07:00:00', 'Race', '2025-03-23 07:00:00', true);
INSERT INTO public.races VALUES (2, 3, 'suzuka', 3, 'Japan', 'Suzuka', 'Japanese Grand Prix', '2025-04-06', 'conventional', 'Practice 1', '2025-04-04 02:30:00', 'Practice 2', '2025-04-04 06:00:00', 'Practice 3', '2025-04-05 02:30:00', 'Qualifying', '2025-04-05 06:00:00', 'Race', '2025-04-06 05:00:00', false);
INSERT INTO public.races VALUES (3, 3, 'jeddah', 5, 'Saudi Arabia', 'Jeddah', 'Saudi Arabian Grand Prix', '2025-04-20', 'conventional', 'Practice 1', '2025-04-18 13:30:00', 'Practice 2', '2025-04-18 17:00:00', 'Practice 3', '2025-04-19 13:30:00', 'Qualifying', '2025-04-19 17:00:00', 'Race', '2025-04-20 17:00:00', false);
INSERT INTO public.races VALUES (9, 3, 'zandvoort', 15, 'Netherlands', 'Zandvoort', 'Dutch Grand Prix', '2025-08-31', 'conventional', 'Practice 1', '2025-08-29 10:30:00', 'Practice 2', '2025-08-29 14:00:00', 'Practice 3', '2025-08-30 09:30:00', 'Qualifying', '2025-08-30 13:00:00', 'Race', '2025-08-31 13:00:00', false);
INSERT INTO public.races VALUES (25, 3, 'bahrain', 0, 'Bahrain', 'Sakhir', 'FORMULA 1 ARAMCO PRE-SEASON TESTING 2025', '2025-02-28', 'testing', 'Practice 1', '2025-02-26 07:00:00', 'Practice 2', '2025-02-27 07:00:00', 'Practice 3', '2025-02-28 07:00:00', 'None', NULL, 'None', NULL, false);
INSERT INTO public.races VALUES (20, 3, 'americas', 19, 'United States', 'Austin', 'United States Grand Prix', '2025-10-19', 'sprint_qualifying', 'Practice 1', '2025-10-17 17:30:00', 'Sprint Qualifying', '2025-10-17 21:30:00', 'Sprint', '2025-10-18 17:00:00', 'Qualifying', '2025-10-18 21:00:00', 'Race', '2025-10-19 19:00:00', true);
INSERT INTO public.races VALUES (13, 3, 'vegas', 22, 'United States', 'Las Vegas', 'Las Vegas Grand Prix', '2025-11-22', 'conventional', 'Practice 1', '2025-11-21 00:30:00', 'Practice 2', '2025-11-21 04:00:00', 'Practice 3', '2025-11-22 00:30:00', 'Qualifying', '2025-11-22 04:00:00', 'Race', '2025-11-23 04:00:00', false);
INSERT INTO public.races VALUES (17, 3, 'villeneuve', 10, 'Canada', 'Montréal', 'Canadian Grand Prix', '2025-06-15', 'conventional', 'Practice 1', '2025-06-13 17:30:00', 'Practice 2', '2025-06-13 21:00:00', 'Practice 3', '2025-06-14 16:30:00', 'Qualifying', '2025-06-14 20:00:00', 'Race', '2025-06-15 18:00:00', false);
INSERT INTO public.races VALUES (23, 3, 'losail', 23, 'Qatar', 'Lusail', 'Qatar Grand Prix', '2025-11-30', 'sprint_qualifying', 'Practice 1', '2025-11-28 13:30:00', 'Sprint Qualifying', '2025-11-28 17:30:00', 'Sprint', '2025-11-29 14:00:00', 'Qualifying', '2025-11-29 18:00:00', 'Race', '2025-11-30 16:00:00', true);
INSERT INTO public.races VALUES (24, 3, 'yas_marina', 24, 'United Arab Emirates', 'Yas Island', 'Abu Dhabi Grand Prix', '2025-12-07', 'conventional', 'Practice 1', '2025-12-05 09:30:00', 'Practice 2', '2025-12-05 13:00:00', 'Practice 3', '2025-12-06 10:30:00', 'Qualifying', '2025-12-06 14:00:00', 'Race', '2025-12-07 13:00:00', false);
INSERT INTO public.races VALUES (10, 3, 'monza', 16, 'Italy', 'Monza', 'Italian Grand Prix', '2025-09-07', 'conventional', 'Practice 1', '2025-09-05 11:30:00', 'Practice 2', '2025-09-05 15:00:00', 'Practice 3', '2025-09-06 10:30:00', 'Qualifying', '2025-09-06 14:00:00', 'Race', '2025-09-07 13:00:00', false);
INSERT INTO public.races VALUES (11, 3, 'baku', 17, 'Azerbaijan', 'Baku', 'Azerbaijan Grand Prix', '2025-09-21', 'conventional', 'Practice 1', '2025-09-19 08:30:00', 'Practice 2', '2025-09-19 12:00:00', 'Practice 3', '2025-09-20 08:30:00', 'Qualifying', '2025-09-20 12:00:00', 'Race', '2025-09-21 11:00:00', false);
INSERT INTO public.races VALUES (12, 3, 'marina_bay', 18, 'Singapore', 'Marina Bay', 'Singapore Grand Prix', '2025-10-05', 'conventional', 'Practice 1', '2025-10-03 09:30:00', 'Practice 2', '2025-10-03 13:00:00', 'Practice 3', '2025-10-04 09:30:00', 'Qualifying', '2025-10-04 13:00:00', 'Race', '2025-10-05 12:00:00', false);
INSERT INTO public.races VALUES (14, 3, 'albert_park', 1, 'Australia', 'Melbourne', 'Australian Grand Prix', '2025-03-16', 'conventional', 'Practice 1', '2025-03-14 01:30:00', 'Practice 2', '2025-03-14 05:00:00', 'Practice 3', '2025-03-15 01:30:00', 'Qualifying', '2025-03-15 05:00:00', 'Race', '2025-03-16 04:00:00', false);
INSERT INTO public.races VALUES (15, 3, 'bahrain', 4, 'Bahrain', 'Sakhir', 'Bahrain Grand Prix', '2025-04-13', 'conventional', 'Practice 1', '2025-04-11 11:30:00', 'Practice 2', '2025-04-11 15:00:00', 'Practice 3', '2025-04-12 12:30:00', 'Qualifying', '2025-04-12 16:00:00', 'Race', '2025-04-13 15:00:00', false);
INSERT INTO public.races VALUES (16, 3, 'imola', 7, 'Italy', 'Imola', 'Emilia Romagna Grand Prix', '2025-05-18', 'conventional', 'Practice 1', '2025-05-16 11:30:00', 'Practice 2', '2025-05-16 15:00:00', 'Practice 3', '2025-05-17 10:30:00', 'Qualifying', '2025-05-17 14:00:00', 'Race', '2025-05-18 13:00:00', false);
INSERT INTO public.races VALUES (18, 3, 'red_bull_ring', 11, 'Austria', 'Spielberg', 'Austrian Grand Prix', '2025-06-29', 'conventional', 'Practice 1', '2025-06-27 11:30:00', 'Practice 2', '2025-06-27 15:00:00', 'Practice 3', '2025-06-28 10:30:00', 'Qualifying', '2025-06-28 14:00:00', 'Race', '2025-06-29 13:00:00', false);
INSERT INTO public.races VALUES (19, 3, 'hungaroring', 14, 'Hungary', 'Budapest', 'Hungarian Grand Prix', '2025-08-03', 'conventional', 'Practice 1', '2025-08-01 11:30:00', 'Practice 2', '2025-08-01 15:00:00', 'Practice 3', '2025-08-02 10:30:00', 'Qualifying', '2025-08-02 14:00:00', 'Race', '2025-08-03 13:00:00', false);
INSERT INTO public.races VALUES (21, 3, 'rodriguez', 20, 'Mexico', 'Mexico City', 'Mexico City Grand Prix', '2025-10-26', 'conventional', 'Practice 1', '2025-10-24 18:30:00', 'Practice 2', '2025-10-24 22:00:00', 'Practice 3', '2025-10-25 17:30:00', 'Qualifying', '2025-10-25 21:00:00', 'Race', '2025-10-26 20:00:00', false);
INSERT INTO public.races VALUES (22, 3, 'interlagos', 21, 'Brazil', 'São Paulo', 'São Paulo Grand Prix', '2025-11-09', 'sprint_qualifying', 'Practice 1', '2025-11-07 14:30:00', 'Sprint Qualifying', '2025-11-07 18:30:00', 'Sprint', '2025-11-08 14:00:00', 'Qualifying', '2025-11-08 18:00:00', 'Race', '2025-11-09 17:00:00', true);


--
-- Data for Name: qualifying_results; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.qualifying_results VALUES (441, 8, 'norris', 'mclaren', 4, 1, '0 days 00:01:41.010000', '0 days 00:01:40.715000', '0 days 00:01:40.562000');
INSERT INTO public.qualifying_results VALUES (442, 8, 'piastri', 'mclaren', 81, 2, '0 days 00:01:41.201000', '0 days 00:01:40.626000', '0 days 00:01:40.647000');
INSERT INTO public.qualifying_results VALUES (443, 8, 'leclerc', 'ferrari', 16, 3, '0 days 00:01:41.635000', '0 days 00:01:41.084000', '0 days 00:01:40.900000');
INSERT INTO public.qualifying_results VALUES (444, 8, 'max_verstappen', 'red_bull', 1, 4, '0 days 00:01:41.334000', '0 days 00:01:40.951000', '0 days 00:01:40.903000');
INSERT INTO public.qualifying_results VALUES (445, 8, 'albon', 'williams', 23, 5, '0 days 00:01:41.772000', '0 days 00:01:41.505000', '0 days 00:01:41.201000');
INSERT INTO public.qualifying_results VALUES (446, 8, 'russell', 'mercedes', 63, 6, '0 days 00:01:41.784000', '0 days 00:01:41.254000', '0 days 00:01:41.260000');
INSERT INTO public.qualifying_results VALUES (447, 8, 'tsunoda', 'red_bull', 22, 7, '0 days 00:01:41.840000', '0 days 00:01:41.245000', '0 days 00:01:41.284000');
INSERT INTO public.qualifying_results VALUES (448, 8, 'hadjar', 'rb', 6, 8, '0 days 00:01:41.572000', '0 days 00:01:41.281000', '0 days 00:01:41.310000');
INSERT INTO public.qualifying_results VALUES (449, 8, 'lawson', 'rb', 30, 9, '0 days 00:01:41.748000', '0 days 00:01:41.297000', '0 days 00:01:41.328000');
INSERT INTO public.qualifying_results VALUES (450, 8, 'bortoleto', 'sauber', 5, 10, '0 days 00:01:41.908000', '0 days 00:01:41.336000', '0 days 00:01:42.387000');
INSERT INTO public.qualifying_results VALUES (451, 8, 'ocon', 'haas', 31, 11, '0 days 00:01:41.884000', '0 days 00:01:41.525000', NULL);
INSERT INTO public.qualifying_results VALUES (452, 8, 'bearman', 'haas', 87, 12, '0 days 00:01:41.617000', '0 days 00:01:41.617000', NULL);
INSERT INTO public.qualifying_results VALUES (453, 8, 'gasly', 'alpine', 10, 13, '0 days 00:01:41.800000', '0 days 00:01:41.633000', NULL);
INSERT INTO public.qualifying_results VALUES (454, 8, 'hulkenberg', 'sauber', 27, 14, '0 days 00:01:41.844000', '0 days 00:01:41.707000', NULL);
INSERT INTO public.qualifying_results VALUES (455, 8, 'sainz', 'williams', 55, 15, '0 days 00:01:41.691000', '0 days 00:01:41.758000', NULL);
INSERT INTO public.qualifying_results VALUES (456, 8, 'hamilton', 'ferrari', 44, 16, '0 days 00:01:41.939000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (457, 8, 'colapinto', 'alpine', 43, 17, '0 days 00:01:42.022000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (458, 8, 'antonelli', 'mercedes', 12, 18, '0 days 00:01:42.139000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (459, 8, 'alonso', 'aston_martin', 14, 19, '0 days 00:01:42.385000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (460, 8, 'stroll', 'aston_martin', 18, 20, '0 days 00:01:42.502000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (461, 19, 'leclerc', 'ferrari', 16, 1, '0 days 00:01:15.582000', '0 days 00:01:15.455000', '0 days 00:01:15.372000');
INSERT INTO public.qualifying_results VALUES (462, 19, 'piastri', 'mclaren', 81, 2, '0 days 00:01:15.211000', '0 days 00:01:14.941000', '0 days 00:01:15.398000');
INSERT INTO public.qualifying_results VALUES (463, 19, 'norris', 'mclaren', 4, 3, '0 days 00:01:15.523000', '0 days 00:01:14.890000', '0 days 00:01:15.413000');
INSERT INTO public.qualifying_results VALUES (464, 19, 'russell', 'mercedes', 63, 4, '0 days 00:01:15.627000', '0 days 00:01:15.201000', '0 days 00:01:15.425000');
INSERT INTO public.qualifying_results VALUES (465, 19, 'alonso', 'aston_martin', 14, 5, '0 days 00:01:15.281000', '0 days 00:01:15.395000', '0 days 00:01:15.481000');
INSERT INTO public.qualifying_results VALUES (466, 19, 'stroll', 'aston_martin', 18, 6, '0 days 00:01:15.673000', '0 days 00:01:15.129000', '0 days 00:01:15.498000');
INSERT INTO public.qualifying_results VALUES (467, 19, 'bortoleto', 'sauber', 5, 7, '0 days 00:01:15.586000', '0 days 00:01:15.687000', '0 days 00:01:15.725000');
INSERT INTO public.qualifying_results VALUES (468, 19, 'max_verstappen', 'red_bull', 1, 8, '0 days 00:01:15.736000', '0 days 00:01:15.547000', '0 days 00:01:15.728000');
INSERT INTO public.qualifying_results VALUES (469, 19, 'hadjar', 'rb', 6, 10, '0 days 00:01:15.516000', '0 days 00:01:15.469000', '0 days 00:01:15.915000');
INSERT INTO public.qualifying_results VALUES (470, 19, 'sainz', 'williams', 55, 13, '0 days 00:01:15.652000', '0 days 00:01:15.781000', NULL);
INSERT INTO public.qualifying_results VALUES (471, 19, 'lawson', 'rb', 30, 9, '0 days 00:01:15.849000', '0 days 00:01:15.630000', '0 days 00:01:15.821000');
INSERT INTO public.qualifying_results VALUES (472, 19, 'bearman', 'haas', 87, 11, '0 days 00:01:15.750000', '0 days 00:01:15.694000', NULL);
INSERT INTO public.qualifying_results VALUES (473, 19, 'hamilton', 'ferrari', 44, 12, '0 days 00:01:15.733000', '0 days 00:01:15.702000', NULL);
INSERT INTO public.qualifying_results VALUES (474, 19, 'colapinto', 'alpine', 43, 14, '0 days 00:01:15.875000', '0 days 00:01:16.159000', NULL);
INSERT INTO public.qualifying_results VALUES (475, 19, 'antonelli', 'mercedes', 12, 15, '0 days 00:01:15.782000', '0 days 00:01:16.386000', NULL);
INSERT INTO public.qualifying_results VALUES (476, 19, 'tsunoda', 'red_bull', 22, 16, '0 days 00:01:15.899000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (477, 19, 'gasly', 'alpine', 10, 17, '0 days 00:01:15.966000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (478, 19, 'ocon', 'haas', 31, 18, '0 days 00:01:16.023000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (479, 19, 'hulkenberg', 'sauber', 27, 19, '0 days 00:01:16.081000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (480, 19, 'albon', 'williams', 23, 20, '0 days 00:01:16.223000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (481, 9, 'piastri', 'mclaren', 81, 1, '0 days 00:01:09.338000', '0 days 00:01:08.964000', '0 days 00:01:08.662000');
INSERT INTO public.qualifying_results VALUES (482, 9, 'norris', 'mclaren', 4, 2, '0 days 00:01:09.469000', '0 days 00:01:08.874000', '0 days 00:01:08.674000');
INSERT INTO public.qualifying_results VALUES (483, 9, 'max_verstappen', 'red_bull', 1, 3, '0 days 00:01:09.696000', '0 days 00:01:09.122000', '0 days 00:01:08.925000');
INSERT INTO public.qualifying_results VALUES (484, 9, 'hadjar', 'rb', 6, 4, '0 days 00:01:09.966000', '0 days 00:01:09.439000', '0 days 00:01:09.208000');
INSERT INTO public.qualifying_results VALUES (485, 9, 'russell', 'mercedes', 63, 5, '0 days 00:01:09.676000', '0 days 00:01:09.313000', '0 days 00:01:09.255000');
INSERT INTO public.qualifying_results VALUES (486, 9, 'leclerc', 'ferrari', 16, 6, '0 days 00:01:09.906000', '0 days 00:01:09.304000', '0 days 00:01:09.340000');
INSERT INTO public.qualifying_results VALUES (487, 9, 'hamilton', 'ferrari', 44, 7, '0 days 00:01:09.900000', '0 days 00:01:09.261000', '0 days 00:01:09.390000');
INSERT INTO public.qualifying_results VALUES (488, 9, 'lawson', 'rb', 30, 8, '0 days 00:01:09.779000', '0 days 00:01:09.383000', '0 days 00:01:09.500000');
INSERT INTO public.qualifying_results VALUES (489, 9, 'sainz', 'williams', 55, 9, '0 days 00:01:09.980000', '0 days 00:01:09.472000', '0 days 00:01:09.505000');
INSERT INTO public.qualifying_results VALUES (490, 9, 'alonso', 'aston_martin', 14, 10, '0 days 00:01:09.950000', '0 days 00:01:09.366000', '0 days 00:01:09.630000');
INSERT INTO public.qualifying_results VALUES (491, 9, 'antonelli', 'mercedes', 12, 11, '0 days 00:01:09.845000', '0 days 00:01:09.493000', NULL);
INSERT INTO public.qualifying_results VALUES (492, 9, 'tsunoda', 'red_bull', 22, 12, '0 days 00:01:09.954000', '0 days 00:01:09.622000', NULL);
INSERT INTO public.qualifying_results VALUES (493, 9, 'bortoleto', 'sauber', 5, 13, '0 days 00:01:10.037000', '0 days 00:01:09.622000', NULL);
INSERT INTO public.qualifying_results VALUES (494, 9, 'gasly', 'alpine', 10, 14, '0 days 00:01:09.894000', '0 days 00:01:09.637000', NULL);
INSERT INTO public.qualifying_results VALUES (495, 9, 'albon', 'williams', 23, 15, '0 days 00:01:09.792000', '0 days 00:01:09.652000', NULL);
INSERT INTO public.qualifying_results VALUES (496, 9, 'colapinto', 'alpine', 43, 16, '0 days 00:01:10.104000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (497, 9, 'hulkenberg', 'sauber', 27, 17, '0 days 00:01:10.195000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (498, 9, 'ocon', 'haas', 31, 18, '0 days 00:01:10.197000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (499, 9, 'bearman', 'haas', 87, 19, '0 days 00:01:10.262000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (500, 9, 'stroll', 'aston_martin', 18, 20, NULL, NULL, NULL);
INSERT INTO public.qualifying_results VALUES (501, 10, 'max_verstappen', 'red_bull', 1, 1, '0 days 00:01:19.455000', '0 days 00:01:19.140000', '0 days 00:01:18.792000');
INSERT INTO public.qualifying_results VALUES (502, 10, 'norris', 'mclaren', 4, 2, '0 days 00:01:19.517000', '0 days 00:01:19.293000', '0 days 00:01:18.869000');
INSERT INTO public.qualifying_results VALUES (503, 10, 'piastri', 'mclaren', 81, 3, '0 days 00:01:19.711000', '0 days 00:01:19.286000', '0 days 00:01:18.982000');
INSERT INTO public.qualifying_results VALUES (504, 10, 'leclerc', 'ferrari', 16, 4, '0 days 00:01:19.689000', '0 days 00:01:19.310000', '0 days 00:01:19.007000');
INSERT INTO public.qualifying_results VALUES (505, 10, 'hamilton', 'ferrari', 44, 5, '0 days 00:01:19.765000', '0 days 00:01:19.371000', '0 days 00:01:19.124000');
INSERT INTO public.qualifying_results VALUES (506, 10, 'russell', 'mercedes', 63, 6, '0 days 00:01:19.414000', '0 days 00:01:19.287000', '0 days 00:01:19.157000');
INSERT INTO public.qualifying_results VALUES (507, 10, 'antonelli', 'mercedes', 12, 7, '0 days 00:01:19.747000', '0 days 00:01:19.245000', '0 days 00:01:19.200000');
INSERT INTO public.qualifying_results VALUES (508, 10, 'bortoleto', 'sauber', 5, 8, '0 days 00:01:19.688000', '0 days 00:01:19.323000', '0 days 00:01:19.390000');
INSERT INTO public.qualifying_results VALUES (509, 10, 'alonso', 'aston_martin', 14, 9, '0 days 00:01:19.658000', '0 days 00:01:19.362000', '0 days 00:01:19.424000');
INSERT INTO public.qualifying_results VALUES (510, 10, 'tsunoda', 'red_bull', 22, 10, '0 days 00:01:19.619000', '0 days 00:01:19.433000', '0 days 00:01:19.519000');
INSERT INTO public.qualifying_results VALUES (511, 10, 'bearman', 'haas', 87, 11, '0 days 00:01:19.688000', '0 days 00:01:19.446000', NULL);
INSERT INTO public.qualifying_results VALUES (512, 10, 'hulkenberg', 'sauber', 27, 12, '0 days 00:01:19.777000', '0 days 00:01:19.498000', NULL);
INSERT INTO public.qualifying_results VALUES (513, 10, 'sainz', 'williams', 55, 13, '0 days 00:01:19.644000', '0 days 00:01:19.528000', NULL);
INSERT INTO public.qualifying_results VALUES (514, 10, 'albon', 'williams', 23, 14, '0 days 00:01:19.837000', '0 days 00:01:19.583000', NULL);
INSERT INTO public.qualifying_results VALUES (515, 10, 'ocon', 'haas', 31, 15, '0 days 00:01:19.816000', '0 days 00:01:19.707000', NULL);
INSERT INTO public.qualifying_results VALUES (516, 10, 'hadjar', 'rb', 6, 16, '0 days 00:01:19.917000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (517, 10, 'stroll', 'aston_martin', 18, 17, '0 days 00:01:19.948000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (518, 10, 'colapinto', 'alpine', 43, 18, '0 days 00:01:19.992000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (519, 10, 'gasly', 'alpine', 10, 19, '0 days 00:01:20.103000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (520, 10, 'lawson', 'rb', 30, 20, '0 days 00:01:20.279000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (521, 11, 'max_verstappen', 'red_bull', 1, 1, '0 days 00:01:41.331000', '0 days 00:01:41.255000', '0 days 00:01:41.117000');
INSERT INTO public.qualifying_results VALUES (522, 11, 'sainz', 'williams', 55, 2, '0 days 00:01:42.635000', '0 days 00:01:41.675000', '0 days 00:01:41.595000');
INSERT INTO public.qualifying_results VALUES (523, 11, 'lawson', 'rb', 30, 3, '0 days 00:01:42.257000', '0 days 00:01:41.537000', '0 days 00:01:41.707000');
INSERT INTO public.qualifying_results VALUES (524, 11, 'antonelli', 'mercedes', 12, 4, '0 days 00:01:42.247000', '0 days 00:01:41.464000', '0 days 00:01:41.717000');
INSERT INTO public.qualifying_results VALUES (525, 11, 'russell', 'mercedes', 63, 5, '0 days 00:01:41.646000', '0 days 00:01:41.455000', '0 days 00:01:42.070000');
INSERT INTO public.qualifying_results VALUES (526, 11, 'norris', 'mclaren', 4, 7, '0 days 00:01:41.322000', '0 days 00:01:41.396000', '0 days 00:01:42.239000');
INSERT INTO public.qualifying_results VALUES (527, 11, 'hadjar', 'rb', 6, 8, '0 days 00:01:41.656000', '0 days 00:01:41.647000', '0 days 00:01:42.372000');
INSERT INTO public.qualifying_results VALUES (528, 11, 'piastri', 'mclaren', 81, 9, '0 days 00:01:41.839000', '0 days 00:01:41.414000', NULL);
INSERT INTO public.qualifying_results VALUES (529, 11, 'leclerc', 'ferrari', 16, 10, '0 days 00:01:41.458000', '0 days 00:01:41.519000', NULL);
INSERT INTO public.qualifying_results VALUES (530, 11, 'hamilton', 'ferrari', 44, 12, '0 days 00:01:41.821000', '0 days 00:01:42.183000', NULL);
INSERT INTO public.qualifying_results VALUES (531, 11, 'tsunoda', 'red_bull', 22, 6, '0 days 00:01:42.347000', '0 days 00:01:41.788000', '0 days 00:01:42.143000');
INSERT INTO public.qualifying_results VALUES (532, 11, 'alonso', 'aston_martin', 14, 11, '0 days 00:01:42.211000', '0 days 00:01:41.857000', NULL);
INSERT INTO public.qualifying_results VALUES (533, 11, 'bortoleto', 'sauber', 5, 13, '0 days 00:01:42.511000', '0 days 00:01:42.277000', NULL);
INSERT INTO public.qualifying_results VALUES (534, 11, 'stroll', 'aston_martin', 18, 14, '0 days 00:01:42.101000', '0 days 00:01:43.061000', NULL);
INSERT INTO public.qualifying_results VALUES (535, 11, 'bearman', 'haas', 87, 15, '0 days 00:01:42.666000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (536, 11, 'colapinto', 'alpine', 43, 16, '0 days 00:01:42.779000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (537, 11, 'hulkenberg', 'sauber', 27, 17, '0 days 00:01:42.916000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (538, 11, 'gasly', 'alpine', 10, 18, '0 days 00:01:43.139000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (539, 11, 'albon', 'williams', 23, 19, '0 days 00:01:43.778000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (540, 11, 'ocon', 'haas', 31, 20, NULL, NULL, NULL);
INSERT INTO public.qualifying_results VALUES (201, 18, 'norris', 'mclaren', 4, 1, '0 days 00:01:04.672000', '0 days 00:01:04.410000', '0 days 00:01:03.971000');
INSERT INTO public.qualifying_results VALUES (202, 18, 'leclerc', 'ferrari', 16, 2, '0 days 00:01:05.197000', '0 days 00:01:04.734000', '0 days 00:01:04.492000');
INSERT INTO public.qualifying_results VALUES (203, 18, 'piastri', 'mclaren', 81, 3, '0 days 00:01:04.966000', '0 days 00:01:04.556000', '0 days 00:01:04.554000');
INSERT INTO public.qualifying_results VALUES (204, 18, 'hamilton', 'ferrari', 44, 4, '0 days 00:01:05.115000', '0 days 00:01:04.896000', '0 days 00:01:04.582000');
INSERT INTO public.qualifying_results VALUES (205, 18, 'russell', 'mercedes', 63, 5, '0 days 00:01:05.189000', '0 days 00:01:04.860000', '0 days 00:01:04.763000');
INSERT INTO public.qualifying_results VALUES (206, 18, 'lawson', 'rb', 30, 6, '0 days 00:01:05.017000', '0 days 00:01:05.041000', '0 days 00:01:04.926000');
INSERT INTO public.qualifying_results VALUES (207, 18, 'max_verstappen', 'red_bull', 1, 7, '0 days 00:01:05.106000', '0 days 00:01:04.836000', '0 days 00:01:04.929000');
INSERT INTO public.qualifying_results VALUES (208, 18, 'bortoleto', 'sauber', 5, 8, '0 days 00:01:05.123000', '0 days 00:01:04.846000', '0 days 00:01:05.132000');
INSERT INTO public.qualifying_results VALUES (209, 18, 'gasly', 'alpine', 10, 10, '0 days 00:01:05.054000', '0 days 00:01:04.846000', '0 days 00:01:05.649000');
INSERT INTO public.qualifying_results VALUES (210, 18, 'hadjar', 'rb', 6, 13, '0 days 00:01:05.063000', '0 days 00:01:05.226000', NULL);
INSERT INTO public.qualifying_results VALUES (211, 18, 'antonelli', 'mercedes', 12, 9, '0 days 00:01:05.178000', '0 days 00:01:05.052000', '0 days 00:01:05.276000');
INSERT INTO public.qualifying_results VALUES (212, 18, 'alonso', 'aston_martin', 14, 11, '0 days 00:01:05.197000', '0 days 00:01:05.128000', NULL);
INSERT INTO public.qualifying_results VALUES (213, 18, 'albon', 'williams', 23, 12, '0 days 00:01:05.143000', '0 days 00:01:05.205000', NULL);
INSERT INTO public.qualifying_results VALUES (214, 18, 'colapinto', 'alpine', 43, 14, '0 days 00:01:05.278000', '0 days 00:01:05.288000', NULL);
INSERT INTO public.qualifying_results VALUES (215, 18, 'bearman', 'haas', 87, 15, '0 days 00:01:05.218000', '0 days 00:01:05.312000', NULL);
INSERT INTO public.qualifying_results VALUES (216, 18, 'stroll', 'aston_martin', 18, 16, '0 days 00:01:05.329000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (217, 18, 'ocon', 'haas', 31, 17, '0 days 00:01:05.364000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (218, 18, 'tsunoda', 'red_bull', 22, 18, '0 days 00:01:05.369000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (219, 18, 'sainz', 'williams', 55, 19, '0 days 00:01:05.582000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (220, 18, 'hulkenberg', 'sauber', 27, 20, '0 days 00:01:05.606000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (221, 7, 'max_verstappen', 'red_bull', 1, 1, '0 days 00:01:25.886000', '0 days 00:01:25.316000', '0 days 00:01:24.892000');
INSERT INTO public.qualifying_results VALUES (222, 7, 'piastri', 'mclaren', 81, 2, '0 days 00:01:25.963000', '0 days 00:01:25.316000', '0 days 00:01:24.995000');
INSERT INTO public.qualifying_results VALUES (223, 7, 'norris', 'mclaren', 4, 3, '0 days 00:01:26.123000', '0 days 00:01:25.231000', '0 days 00:01:25.010000');
INSERT INTO public.qualifying_results VALUES (224, 7, 'russell', 'mercedes', 63, 4, '0 days 00:01:26.236000', '0 days 00:01:25.637000', '0 days 00:01:25.029000');
INSERT INTO public.qualifying_results VALUES (225, 7, 'hamilton', 'ferrari', 44, 5, '0 days 00:01:26.296000', '0 days 00:01:25.084000', '0 days 00:01:25.095000');
INSERT INTO public.qualifying_results VALUES (226, 7, 'leclerc', 'ferrari', 16, 6, '0 days 00:01:26.186000', '0 days 00:01:25.133000', '0 days 00:01:25.121000');
INSERT INTO public.qualifying_results VALUES (227, 7, 'antonelli', 'mercedes', 12, 7, '0 days 00:01:26.265000', '0 days 00:01:25.620000', '0 days 00:01:25.374000');
INSERT INTO public.qualifying_results VALUES (228, 7, 'bearman', 'haas', 87, 8, '0 days 00:01:26.005000', '0 days 00:01:25.534000', '0 days 00:01:25.471000');
INSERT INTO public.qualifying_results VALUES (229, 7, 'alonso', 'aston_martin', 14, 9, '0 days 00:01:26.108000', '0 days 00:01:25.593000', '0 days 00:01:25.621000');
INSERT INTO public.qualifying_results VALUES (230, 7, 'gasly', 'alpine', 10, 10, '0 days 00:01:26.328000', '0 days 00:01:25.711000', '0 days 00:01:25.785000');
INSERT INTO public.qualifying_results VALUES (231, 7, 'sainz', 'williams', 55, 11, '0 days 00:01:26.175000', '0 days 00:01:25.746000', NULL);
INSERT INTO public.qualifying_results VALUES (232, 7, 'tsunoda', 'red_bull', 22, 12, '0 days 00:01:26.275000', '0 days 00:01:25.826000', NULL);
INSERT INTO public.qualifying_results VALUES (233, 7, 'hadjar', 'rb', 6, 13, '0 days 00:01:26.177000', '0 days 00:01:25.864000', NULL);
INSERT INTO public.qualifying_results VALUES (234, 7, 'albon', 'williams', 23, 14, '0 days 00:01:26.093000', '0 days 00:01:25.889000', NULL);
INSERT INTO public.qualifying_results VALUES (235, 7, 'ocon', 'haas', 31, 15, '0 days 00:01:26.136000', '0 days 00:01:25.950000', NULL);
INSERT INTO public.qualifying_results VALUES (236, 7, 'lawson', 'rb', 30, 16, '0 days 00:01:26.440000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (237, 7, 'bortoleto', 'sauber', 5, 17, '0 days 00:01:26.446000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (238, 7, 'stroll', 'aston_martin', 18, 18, '0 days 00:01:26.504000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (239, 7, 'hulkenberg', 'sauber', 27, 19, '0 days 00:01:26.574000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (240, 7, 'colapinto', 'alpine', 43, 20, '0 days 00:01:27.060000', NULL, NULL);
INSERT INTO public.qualifying_results VALUES (241, 14, 'norris', 'mclaren', 4, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (242, 14, 'piastri', 'mclaren', 81, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (243, 14, 'max_verstappen', 'red_bull', 1, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (244, 14, 'russell', 'mercedes', 63, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (245, 14, 'tsunoda', 'rb', 22, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (246, 14, 'albon', 'williams', 23, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (247, 14, 'leclerc', 'ferrari', 16, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (248, 14, 'hamilton', 'ferrari', 44, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (249, 14, 'gasly', 'alpine', 10, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (250, 14, 'sainz', 'williams', 55, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (251, 14, 'hadjar', 'rb', 6, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (252, 14, 'alonso', 'aston_martin', 14, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (253, 14, 'stroll', 'aston_martin', 18, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (254, 14, 'doohan', 'alpine', 7, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (255, 14, 'bortoleto', 'sauber', 5, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (256, 14, 'antonelli', 'mercedes', 12, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (257, 14, 'hulkenberg', 'sauber', 27, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (258, 14, 'lawson', 'red_bull', 30, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (259, 14, 'ocon', 'haas', 31, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (260, 14, 'bearman', 'haas', 87, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (261, 1, 'piastri', 'mclaren', 81, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (262, 1, 'russell', 'mercedes', 63, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (263, 1, 'norris', 'mclaren', 4, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (264, 1, 'max_verstappen', 'red_bull', 1, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (265, 1, 'hamilton', 'ferrari', 44, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (266, 1, 'leclerc', 'ferrari', 16, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (267, 1, 'hadjar', 'rb', 6, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (268, 1, 'antonelli', 'mercedes', 12, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (269, 1, 'tsunoda', 'rb', 22, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (270, 1, 'albon', 'williams', 23, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (271, 1, 'ocon', 'haas', 31, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (272, 1, 'hulkenberg', 'sauber', 27, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (273, 1, 'alonso', 'aston_martin', 14, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (274, 1, 'stroll', 'aston_martin', 18, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (275, 1, 'sainz', 'williams', 55, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (276, 1, 'gasly', 'alpine', 10, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (277, 1, 'bearman', 'haas', 87, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (278, 1, 'doohan', 'alpine', 7, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (279, 1, 'bortoleto', 'sauber', 5, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (280, 1, 'lawson', 'red_bull', 30, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (281, 2, 'max_verstappen', 'red_bull', 1, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (282, 2, 'norris', 'mclaren', 4, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (283, 2, 'piastri', 'mclaren', 81, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (284, 2, 'leclerc', 'ferrari', 16, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (285, 2, 'russell', 'mercedes', 63, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (286, 2, 'antonelli', 'mercedes', 12, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (287, 2, 'hadjar', 'rb', 6, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (288, 2, 'hamilton', 'ferrari', 44, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (289, 2, 'albon', 'williams', 23, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (290, 2, 'bearman', 'haas', 87, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (291, 2, 'gasly', 'alpine', 10, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (292, 2, 'sainz', 'williams', 55, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (293, 2, 'alonso', 'aston_martin', 14, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (294, 2, 'lawson', 'rb', 30, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (295, 2, 'tsunoda', 'red_bull', 22, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (296, 2, 'hulkenberg', 'sauber', 27, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (297, 2, 'bortoleto', 'sauber', 5, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (298, 2, 'ocon', 'haas', 31, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (299, 2, 'doohan', 'alpine', 7, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (300, 2, 'stroll', 'aston_martin', 18, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (301, 15, 'piastri', 'mclaren', 81, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (302, 15, 'russell', 'mercedes', 63, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (303, 15, 'leclerc', 'ferrari', 16, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (304, 15, 'antonelli', 'mercedes', 12, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (305, 15, 'gasly', 'alpine', 10, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (306, 15, 'norris', 'mclaren', 4, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (307, 15, 'max_verstappen', 'red_bull', 1, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (308, 15, 'sainz', 'williams', 55, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (309, 15, 'hamilton', 'ferrari', 44, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (310, 15, 'tsunoda', 'red_bull', 22, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (311, 15, 'doohan', 'alpine', 7, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (312, 15, 'hadjar', 'rb', 6, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (313, 15, 'alonso', 'aston_martin', 14, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (314, 15, 'ocon', 'haas', 31, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (315, 15, 'albon', 'williams', 23, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (316, 15, 'hulkenberg', 'sauber', 27, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (317, 15, 'lawson', 'rb', 30, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (318, 15, 'bortoleto', 'sauber', 5, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (319, 15, 'stroll', 'aston_martin', 18, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (320, 15, 'bearman', 'haas', 87, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (321, 3, 'max_verstappen', 'red_bull', 1, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (322, 3, 'piastri', 'mclaren', 81, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (323, 3, 'russell', 'mercedes', 63, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (324, 3, 'leclerc', 'ferrari', 16, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (325, 3, 'antonelli', 'mercedes', 12, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (326, 3, 'sainz', 'williams', 55, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (327, 3, 'hamilton', 'ferrari', 44, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (328, 3, 'tsunoda', 'red_bull', 22, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (329, 3, 'gasly', 'alpine', 10, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (330, 3, 'norris', 'mclaren', 4, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (331, 3, 'albon', 'williams', 23, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (332, 3, 'lawson', 'rb', 30, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (333, 3, 'alonso', 'aston_martin', 14, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (334, 3, 'hadjar', 'rb', 6, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (335, 3, 'bearman', 'haas', 87, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (336, 3, 'stroll', 'aston_martin', 18, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (337, 3, 'doohan', 'alpine', 7, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (338, 3, 'hulkenberg', 'sauber', 27, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (339, 3, 'ocon', 'haas', 31, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (340, 3, 'bortoleto', 'sauber', 5, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (341, 4, 'max_verstappen', 'red_bull', 1, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (342, 4, 'norris', 'mclaren', 4, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (343, 4, 'antonelli', 'mercedes', 12, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (344, 4, 'piastri', 'mclaren', 81, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (345, 4, 'russell', 'mercedes', 63, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (346, 4, 'sainz', 'williams', 55, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (347, 4, 'albon', 'williams', 23, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (348, 4, 'leclerc', 'ferrari', 16, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (349, 4, 'ocon', 'haas', 31, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (350, 4, 'tsunoda', 'red_bull', 22, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (351, 4, 'hadjar', 'rb', 6, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (352, 4, 'hamilton', 'ferrari', 44, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (353, 4, 'bortoleto', 'sauber', 5, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (354, 4, 'doohan', 'alpine', 7, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (355, 4, 'lawson', 'rb', 30, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (356, 4, 'hulkenberg', 'sauber', 27, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (357, 4, 'alonso', 'aston_martin', 14, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (358, 4, 'gasly', 'alpine', 10, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (359, 4, 'stroll', 'aston_martin', 18, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (360, 4, 'bearman', 'haas', 87, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (361, 16, 'piastri', 'mclaren', 81, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (362, 16, 'max_verstappen', 'red_bull', 1, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (363, 16, 'russell', 'mercedes', 63, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (364, 16, 'norris', 'mclaren', 4, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (365, 16, 'alonso', 'aston_martin', 14, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (366, 16, 'sainz', 'williams', 55, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (367, 16, 'albon', 'williams', 23, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (368, 16, 'stroll', 'aston_martin', 18, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (369, 16, 'hadjar', 'rb', 6, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (370, 16, 'gasly', 'alpine', 10, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (371, 16, 'leclerc', 'ferrari', 16, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (372, 16, 'hamilton', 'ferrari', 44, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (373, 16, 'antonelli', 'mercedes', 12, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (374, 16, 'bortoleto', 'sauber', 5, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (375, 16, 'colapinto', 'alpine', 43, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (376, 16, 'lawson', 'rb', 30, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (377, 16, 'hulkenberg', 'sauber', 27, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (378, 16, 'ocon', 'haas', 31, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (379, 16, 'bearman', 'haas', 87, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (380, 16, 'tsunoda', 'red_bull', 22, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (381, 5, 'norris', 'mclaren', 4, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (382, 5, 'leclerc', 'ferrari', 16, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (383, 5, 'piastri', 'mclaren', 81, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (384, 5, 'hamilton', 'ferrari', 44, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (385, 5, 'max_verstappen', 'red_bull', 1, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (386, 5, 'hadjar', 'rb', 6, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (387, 5, 'alonso', 'aston_martin', 14, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (388, 5, 'ocon', 'haas', 31, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (389, 5, 'lawson', 'rb', 30, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (390, 5, 'albon', 'williams', 23, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (391, 5, 'sainz', 'williams', 55, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (392, 5, 'tsunoda', 'red_bull', 22, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (393, 5, 'hulkenberg', 'sauber', 27, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (394, 5, 'russell', 'mercedes', 63, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (395, 5, 'antonelli', 'mercedes', 12, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (396, 5, 'bortoleto', 'sauber', 5, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (397, 5, 'bearman', 'haas', 87, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (398, 5, 'gasly', 'alpine', 10, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (399, 5, 'stroll', 'aston_martin', 18, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (400, 5, 'colapinto', 'alpine', 43, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (401, 6, 'piastri', 'mclaren', 81, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (402, 6, 'norris', 'mclaren', 4, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (403, 6, 'max_verstappen', 'red_bull', 1, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (404, 6, 'russell', 'mercedes', 63, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (405, 6, 'hamilton', 'ferrari', 44, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (406, 6, 'antonelli', 'mercedes', 12, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (407, 6, 'leclerc', 'ferrari', 16, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (408, 6, 'gasly', 'alpine', 10, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (409, 6, 'hadjar', 'rb', 6, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (410, 6, 'alonso', 'aston_martin', 14, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (411, 6, 'albon', 'williams', 23, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (412, 6, 'bortoleto', 'sauber', 5, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (413, 6, 'lawson', 'rb', 30, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (414, 6, 'stroll', 'aston_martin', 18, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (415, 6, 'bearman', 'haas', 87, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (416, 6, 'hulkenberg', 'sauber', 27, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (417, 6, 'ocon', 'haas', 31, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (418, 6, 'sainz', 'williams', 55, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (419, 6, 'colapinto', 'alpine', 43, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (420, 6, 'tsunoda', 'red_bull', 22, 20, '', '', '');
INSERT INTO public.qualifying_results VALUES (421, 17, 'russell', 'mercedes', 63, 1, '', '', '');
INSERT INTO public.qualifying_results VALUES (422, 17, 'max_verstappen', 'red_bull', 1, 2, '', '', '');
INSERT INTO public.qualifying_results VALUES (423, 17, 'piastri', 'mclaren', 81, 3, '', '', '');
INSERT INTO public.qualifying_results VALUES (424, 17, 'antonelli', 'mercedes', 12, 4, '', '', '');
INSERT INTO public.qualifying_results VALUES (425, 17, 'hamilton', 'ferrari', 44, 5, '', '', '');
INSERT INTO public.qualifying_results VALUES (426, 17, 'alonso', 'aston_martin', 14, 6, '', '', '');
INSERT INTO public.qualifying_results VALUES (427, 17, 'norris', 'mclaren', 4, 7, '', '', '');
INSERT INTO public.qualifying_results VALUES (428, 17, 'leclerc', 'ferrari', 16, 8, '', '', '');
INSERT INTO public.qualifying_results VALUES (429, 17, 'hadjar', 'rb', 6, 9, '', '', '');
INSERT INTO public.qualifying_results VALUES (430, 17, 'albon', 'williams', 23, 10, '', '', '');
INSERT INTO public.qualifying_results VALUES (431, 17, 'tsunoda', 'red_bull', 22, 11, '', '', '');
INSERT INTO public.qualifying_results VALUES (432, 17, 'colapinto', 'alpine', 43, 12, '', '', '');
INSERT INTO public.qualifying_results VALUES (433, 17, 'hulkenberg', 'sauber', 27, 13, '', '', '');
INSERT INTO public.qualifying_results VALUES (434, 17, 'bearman', 'haas', 87, 14, '', '', '');
INSERT INTO public.qualifying_results VALUES (435, 17, 'ocon', 'haas', 31, 15, '', '', '');
INSERT INTO public.qualifying_results VALUES (436, 17, 'bortoleto', 'sauber', 5, 16, '', '', '');
INSERT INTO public.qualifying_results VALUES (437, 17, 'sainz', 'williams', 55, 17, '', '', '');
INSERT INTO public.qualifying_results VALUES (438, 17, 'stroll', 'aston_martin', 18, 18, '', '', '');
INSERT INTO public.qualifying_results VALUES (439, 17, 'lawson', 'rb', 30, 19, '', '', '');
INSERT INTO public.qualifying_results VALUES (440, 17, 'gasly', 'alpine', 10, 20, '', '', '');


--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.results VALUES (1, 14, 'norris', 'mclaren', 4, 1, '1', 25, 1, 57, 'Finished', 6126304, '0 days 01:42:06.304000', 1, 43, '0 days 00:01:22.167000');
INSERT INTO public.results VALUES (2, 14, 'max_verstappen', 'red_bull', 1, 2, '2', 18, 3, 57, 'Finished', 6127199, '0 days 00:00:00.895000', 3, 43, '0 days 00:01:23.081000');
INSERT INTO public.results VALUES (3, 14, 'russell', 'mercedes', 63, 3, '3', 15, 4, 57, 'Finished', 6134785, '0 days 00:00:08.481000', 11, 43, '0 days 00:01:25.065000');
INSERT INTO public.results VALUES (4, 14, 'antonelli', 'mercedes', 12, 4, '4', 12, 16, 57, 'Finished', 6136439, '0 days 00:00:10.135000', 9, 43, '0 days 00:01:24.901000');
INSERT INTO public.results VALUES (5, 14, 'albon', 'williams', 23, 5, '5', 10, 6, 57, 'Finished', 6139077, '0 days 00:00:12.773000', 8, 43, '0 days 00:01:24.597000');
INSERT INTO public.results VALUES (6, 14, 'stroll', 'aston_martin', 18, 6, '6', 8, 13, 57, 'Finished', 6143717, '0 days 00:00:17.413000', 14, 43, '0 days 00:01:25.538000');
INSERT INTO public.results VALUES (7, 14, 'hulkenberg', 'sauber', 27, 7, '7', 6, 17, 57, 'Finished', 6144727, '0 days 00:00:18.423000', 12, 43, '0 days 00:01:25.243000');
INSERT INTO public.results VALUES (8, 14, 'leclerc', 'ferrari', 16, 8, '8', 4, 7, 57, 'Finished', 6146130, '0 days 00:00:19.826000', 13, 43, '0 days 00:01:25.271000');
INSERT INTO public.results VALUES (9, 14, 'piastri', 'mclaren', 81, 9, '9', 2, 2, 57, 'Finished', 6146752, '0 days 00:00:20.448000', 4, 43, '0 days 00:01:23.242000');
INSERT INTO public.results VALUES (10, 14, 'hamilton', 'ferrari', 44, 10, '10', 1, 8, 57, 'Finished', 6148777, '0 days 00:00:22.473000', 7, 43, '0 days 00:01:24.218000');
INSERT INTO public.results VALUES (11, 14, 'gasly', 'alpine', 10, 11, '11', 0, 9, 57, 'Finished', 6152806, '0 days 00:00:26.502000', 10, 43, '0 days 00:01:25.020000');
INSERT INTO public.results VALUES (12, 14, 'tsunoda', 'rb', 22, 12, '12', 0, 5, 57, 'Finished', 6156188, '0 days 00:00:29.884000', 6, 43, '0 days 00:01:24.194000');
INSERT INTO public.results VALUES (13, 14, 'ocon', 'haas', 31, 13, '13', 0, 19, 57, 'Finished', 6159465, '0 days 00:00:33.161000', 15, 42, '0 days 00:01:26.764000');
INSERT INTO public.results VALUES (14, 14, 'bearman', 'haas', 87, 14, '14', 0, 20, 57, 'Finished', 6166655, '0 days 00:00:40.351000', 16, 42, '0 days 00:01:27.603000');
INSERT INTO public.results VALUES (15, 14, 'lawson', 'red_bull', 30, 15, 'R', 0, 18, 46, 'Retired', NULL, NULL, 2, 43, '0 days 00:01:22.970000');
INSERT INTO public.results VALUES (16, 14, 'bortoleto', 'sauber', 5, 16, 'R', 0, 15, 45, 'Retired', NULL, NULL, 5, 43, '0 days 00:01:24.192000');
INSERT INTO public.results VALUES (17, 14, 'alonso', 'aston_martin', 14, 17, 'R', 0, 12, 32, 'Retired', NULL, NULL, 17, 32, '0 days 00:01:28.819000');
INSERT INTO public.results VALUES (18, 14, 'sainz', 'williams', 55, 18, 'R', 0, 10, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (19, 14, 'doohan', 'alpine', 7, 19, 'R', 0, 14, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (20, 14, 'hadjar', 'rb', 6, 20, 'R', 0, 11, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (21, 1, 'piastri', 'mclaren', 81, 1, '1', 25, 1, 56, 'Finished', 5455026, '0 days 01:30:55.026000', 3, 53, '0 days 00:01:35.520000');
INSERT INTO public.results VALUES (22, 1, 'norris', 'mclaren', 4, 2, '2', 18, 3, 56, 'Finished', 5464774, '0 days 00:00:09.748000', 1, 53, '0 days 00:01:35.454000');
INSERT INTO public.results VALUES (23, 1, 'russell', 'mercedes', 63, 3, '3', 15, 2, 56, 'Finished', 5466123, '0 days 00:00:11.097000', 5, 55, '0 days 00:01:35.816000');
INSERT INTO public.results VALUES (24, 1, 'max_verstappen', 'red_bull', 1, 4, '4', 12, 4, 56, 'Finished', 5471682, '0 days 00:00:16.656000', 2, 56, '0 days 00:01:35.488000');
INSERT INTO public.results VALUES (25, 1, 'ocon', 'haas', 31, 5, '5', 10, 11, 56, 'Finished', 5504995, '0 days 00:00:49.969000', 4, 56, '0 days 00:01:35.740000');
INSERT INTO public.results VALUES (26, 1, 'antonelli', 'mercedes', 12, 6, '6', 8, 8, 56, 'Finished', 5508774, '0 days 00:00:53.748000', 11, 56, '0 days 00:01:36.046000');
INSERT INTO public.results VALUES (27, 1, 'albon', 'williams', 23, 7, '7', 6, 10, 56, 'Finished', 5511347, '0 days 00:00:56.321000', 12, 52, '0 days 00:01:36.254000');
INSERT INTO public.results VALUES (28, 1, 'bearman', 'haas', 87, 8, '8', 4, 17, 56, 'Finished', 5516329, '0 days 00:01:01.303000', 13, 52, '0 days 00:01:36.363000');
INSERT INTO public.results VALUES (29, 1, 'stroll', 'aston_martin', 18, 9, '9', 2, 14, 56, 'Finished', 5525230, '0 days 00:01:10.204000', 10, 39, '0 days 00:01:36.044000');
INSERT INTO public.results VALUES (30, 1, 'sainz', 'williams', 55, 10, '10', 1, 15, 56, 'Finished', 5531413, '0 days 00:01:16.387000', 15, 50, '0 days 00:01:36.779000');
INSERT INTO public.results VALUES (31, 1, 'hadjar', 'rb', 6, 11, '11', 0, 7, 56, 'Finished', 5533901, '0 days 00:01:18.875000', 6, 35, '0 days 00:01:35.868000');
INSERT INTO public.results VALUES (32, 1, 'lawson', 'red_bull', 30, 12, '12', 0, 20, 56, 'Finished', 5536173, '0 days 00:01:21.147000', 9, 32, '0 days 00:01:35.985000');
INSERT INTO public.results VALUES (33, 1, 'doohan', 'alpine', 7, 13, '13', 0, 18, 56, 'Finished', 5543427, '0 days 00:01:28.401000', 14, 52, '0 days 00:01:36.424000');
INSERT INTO public.results VALUES (34, 1, 'bortoleto', 'sauber', 5, 14, '14', 0, 19, 55, 'Lapped', 5465782, '0 days 00:00:10.756000', 8, 28, '0 days 00:01:35.874000');
INSERT INTO public.results VALUES (35, 1, 'hulkenberg', 'sauber', 27, 15, '15', 0, 12, 55, 'Lapped', 5475252, '0 days 00:00:20.226000', 16, 35, '0 days 00:01:37.275000');
INSERT INTO public.results VALUES (36, 1, 'tsunoda', 'rb', 22, 16, '16', 0, 9, 55, 'Lapped', 5478537, '0 days 00:00:23.511000', 7, 49, '0 days 00:01:35.871000');
INSERT INTO public.results VALUES (37, 1, 'alonso', 'aston_martin', 14, 17, 'R', 0, 13, 4, 'Retired', NULL, NULL, 17, 3, '0 days 00:01:39.256000');
INSERT INTO public.results VALUES (38, 1, 'leclerc', 'ferrari', 16, 18, 'D', 0, 6, 0, 'Disqualified', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (39, 1, 'hamilton', 'ferrari', 44, 19, 'D', 0, 5, 0, 'Disqualified', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (40, 1, 'gasly', 'alpine', 10, 20, 'D', 0, 16, 0, 'Disqualified', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (41, 2, 'max_verstappen', 'red_bull', 1, 1, '1', 25, 1, 53, 'Finished', 4926983, '0 days 01:22:06.983000', 3, 52, '0 days 00:01:31.041000');
INSERT INTO public.results VALUES (42, 2, 'norris', 'mclaren', 4, 2, '2', 18, 2, 53, 'Finished', 4928406, '0 days 00:00:01.423000', 5, 51, '0 days 00:01:31.116000');
INSERT INTO public.results VALUES (43, 2, 'piastri', 'mclaren', 81, 3, '3', 15, 3, 53, 'Finished', 4929112, '0 days 00:00:02.129000', 2, 53, '0 days 00:01:31.039000');
INSERT INTO public.results VALUES (44, 2, 'leclerc', 'ferrari', 16, 4, '4', 12, 4, 53, 'Finished', 4943080, '0 days 00:00:16.097000', 10, 47, '0 days 00:01:31.469000');
INSERT INTO public.results VALUES (45, 2, 'russell', 'mercedes', 63, 5, '5', 10, 5, 53, 'Finished', 4944345, '0 days 00:00:17.362000', 8, 51, '0 days 00:01:31.357000');
INSERT INTO public.results VALUES (46, 2, 'antonelli', 'mercedes', 12, 6, '6', 8, 6, 53, 'Finished', 4945654, '0 days 00:00:18.671000', 1, 50, '0 days 00:01:30.965000');
INSERT INTO public.results VALUES (47, 2, 'hamilton', 'ferrari', 44, 7, '7', 6, 8, 53, 'Finished', 4956165, '0 days 00:00:29.182000', 9, 51, '0 days 00:01:31.406000');
INSERT INTO public.results VALUES (48, 2, 'hadjar', 'rb', 6, 8, '8', 4, 7, 53, 'Finished', 4964117, '0 days 00:00:37.134000', 7, 52, '0 days 00:01:31.317000');
INSERT INTO public.results VALUES (49, 2, 'albon', 'williams', 23, 9, '9', 2, 9, 53, 'Finished', 4967350, '0 days 00:00:40.367000', 6, 52, '0 days 00:01:31.125000');
INSERT INTO public.results VALUES (50, 2, 'bearman', 'haas', 87, 10, '10', 1, 10, 53, 'Finished', 4981512, '0 days 00:00:54.529000', 15, 49, '0 days 00:01:32.006000');
INSERT INTO public.results VALUES (51, 2, 'alonso', 'aston_martin', 14, 11, '11', 0, 12, 53, 'Finished', 4984316, '0 days 00:00:57.333000', 11, 51, '0 days 00:01:31.770000');
INSERT INTO public.results VALUES (52, 2, 'tsunoda', 'red_bull', 22, 12, '12', 0, 14, 53, 'Finished', 4985384, '0 days 00:00:58.401000', 13, 51, '0 days 00:01:31.871000');
INSERT INTO public.results VALUES (53, 2, 'gasly', 'alpine', 10, 13, '13', 0, 11, 53, 'Finished', 4989105, '0 days 00:01:02.122000', 12, 52, '0 days 00:01:31.820000');
INSERT INTO public.results VALUES (54, 2, 'sainz', 'williams', 55, 14, '14', 0, 15, 53, 'Finished', 5001112, '0 days 00:01:14.129000', 4, 36, '0 days 00:01:31.106000');
INSERT INTO public.results VALUES (55, 2, 'doohan', 'alpine', 7, 15, '15', 0, 19, 53, 'Finished', 5008297, '0 days 00:01:21.314000', 20, 47, '0 days 00:01:32.685000');
INSERT INTO public.results VALUES (56, 2, 'hulkenberg', 'sauber', 27, 16, '16', 0, 16, 53, 'Finished', 5008940, '0 days 00:01:21.957000', 19, 31, '0 days 00:01:32.572000');
INSERT INTO public.results VALUES (57, 2, 'lawson', 'rb', 30, 17, '17', 0, 13, 53, 'Finished', 5009717, '0 days 00:01:22.734000', 17, 39, '0 days 00:01:32.043000');
INSERT INTO public.results VALUES (58, 2, 'ocon', 'haas', 31, 18, '18', 0, 18, 53, 'Finished', 5010421, '0 days 00:01:23.438000', 14, 48, '0 days 00:01:31.967000');
INSERT INTO public.results VALUES (59, 2, 'bortoleto', 'sauber', 5, 19, '19', 0, 17, 53, 'Finished', 5010880, '0 days 00:01:23.897000', 16, 45, '0 days 00:01:32.034000');
INSERT INTO public.results VALUES (60, 2, 'stroll', 'aston_martin', 18, 20, '20', 0, 20, 52, 'Lapped', 4939912, '0 days 00:00:12.929000', 18, 52, '0 days 00:01:32.052000');
INSERT INTO public.results VALUES (61, 15, 'piastri', 'mclaren', 81, 1, '1', 25, 1, 57, 'Finished', 5739435, '0 days 01:35:39.435000', 1, 36, '0 days 00:01:35.140000');
INSERT INTO public.results VALUES (62, 15, 'russell', 'mercedes', 63, 2, '2', 18, 3, 57, 'Finished', 5754934, '0 days 00:00:15.499000', 2, 36, '0 days 00:01:35.518000');
INSERT INTO public.results VALUES (63, 15, 'norris', 'mclaren', 4, 3, '3', 15, 6, 57, 'Finished', 5755708, '0 days 00:00:16.273000', 3, 38, '0 days 00:01:35.728000');
INSERT INTO public.results VALUES (64, 15, 'leclerc', 'ferrari', 16, 4, '4', 12, 2, 57, 'Finished', 5759114, '0 days 00:00:19.679000', 4, 36, '0 days 00:01:36.132000');
INSERT INTO public.results VALUES (65, 15, 'hamilton', 'ferrari', 44, 5, '5', 10, 9, 57, 'Finished', 5767428, '0 days 00:00:27.993000', 6, 37, '0 days 00:01:36.235000');
INSERT INTO public.results VALUES (66, 15, 'max_verstappen', 'red_bull', 1, 6, '6', 8, 7, 57, 'Finished', 5773830, '0 days 00:00:34.395000', 5, 29, '0 days 00:01:36.167000');
INSERT INTO public.results VALUES (67, 15, 'gasly', 'alpine', 10, 7, '7', 6, 4, 57, 'Finished', 5775437, '0 days 00:00:36.002000', 7, 39, '0 days 00:01:36.531000');
INSERT INTO public.results VALUES (68, 15, 'ocon', 'haas', 31, 8, '8', 4, 14, 57, 'Finished', 5783679, '0 days 00:00:44.244000', 12, 30, '0 days 00:01:37.098000');
INSERT INTO public.results VALUES (69, 15, 'tsunoda', 'red_bull', 22, 9, '9', 2, 10, 57, 'Finished', 5784496, '0 days 00:00:45.061000', 14, 45, '0 days 00:01:37.225000');
INSERT INTO public.results VALUES (70, 15, 'bearman', 'haas', 87, 10, '10', 1, 20, 57, 'Finished', 5787029, '0 days 00:00:47.594000', 15, 40, '0 days 00:01:37.303000');
INSERT INTO public.results VALUES (71, 15, 'antonelli', 'mercedes', 12, 11, '11', 0, 5, 57, 'Finished', 5787451, '0 days 00:00:48.016000', 9, 29, '0 days 00:01:36.690000');
INSERT INTO public.results VALUES (72, 15, 'albon', 'williams', 23, 12, '12', 0, 15, 57, 'Finished', 5788274, '0 days 00:00:48.839000', 13, 47, '0 days 00:01:37.141000');
INSERT INTO public.results VALUES (73, 15, 'hadjar', 'rb', 6, 13, '13', 0, 12, 57, 'Finished', 5795749, '0 days 00:00:56.314000', 10, 30, '0 days 00:01:36.952000');
INSERT INTO public.results VALUES (74, 15, 'doohan', 'alpine', 7, 14, '14', 0, 11, 57, 'Finished', 5797241, '0 days 00:00:57.806000', 8, 31, '0 days 00:01:36.682000');
INSERT INTO public.results VALUES (75, 15, 'alonso', 'aston_martin', 14, 15, '15', 0, 13, 57, 'Finished', 5799775, '0 days 00:01:00.340000', 17, 38, '0 days 00:01:37.906000');
INSERT INTO public.results VALUES (76, 15, 'lawson', 'rb', 30, 16, '16', 0, 17, 57, 'Finished', 5803870, '0 days 00:01:04.435000', 16, 44, '0 days 00:01:37.380000');
INSERT INTO public.results VALUES (77, 15, 'stroll', 'aston_martin', 18, 17, '17', 0, 19, 57, 'Finished', 5804924, '0 days 00:01:05.489000', 19, 38, '0 days 00:01:38.064000');
INSERT INTO public.results VALUES (78, 15, 'bortoleto', 'sauber', 5, 18, '18', 0, 18, 57, 'Finished', 5806307, '0 days 00:01:06.872000', 18, 38, '0 days 00:01:38.006000');
INSERT INTO public.results VALUES (79, 15, 'sainz', 'williams', 55, 19, 'R', 0, 8, 45, 'Retired', NULL, NULL, 11, 16, '0 days 00:01:36.954000');
INSERT INTO public.results VALUES (80, 15, 'hulkenberg', 'sauber', 27, 20, 'D', 0, 16, 0, 'Disqualified', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (81, 3, 'piastri', 'mclaren', 81, 1, '1', 25, 2, 50, 'Finished', 4866758, '0 days 01:21:06.758000', 3, 50, '0 days 00:01:32.228000');
INSERT INTO public.results VALUES (82, 3, 'max_verstappen', 'red_bull', 1, 2, '2', 18, 1, 50, 'Finished', 4869601, '0 days 00:00:02.843000', 4, 49, '0 days 00:01:32.280000');
INSERT INTO public.results VALUES (83, 3, 'leclerc', 'ferrari', 16, 3, '3', 15, 4, 50, 'Finished', 4874862, '0 days 00:00:08.104000', 2, 49, '0 days 00:01:32.192000');
INSERT INTO public.results VALUES (84, 3, 'norris', 'mclaren', 4, 4, '4', 12, 10, 50, 'Finished', 4875954, '0 days 00:00:09.196000', 1, 41, '0 days 00:01:31.778000');
INSERT INTO public.results VALUES (85, 3, 'russell', 'mercedes', 63, 5, '5', 10, 3, 50, 'Finished', 4893994, '0 days 00:00:27.236000', 9, 32, '0 days 00:01:32.893000');
INSERT INTO public.results VALUES (86, 3, 'antonelli', 'mercedes', 12, 6, '6', 8, 5, 50, 'Finished', 4901446, '0 days 00:00:34.688000', 5, 50, '0 days 00:01:32.396000');
INSERT INTO public.results VALUES (87, 3, 'hamilton', 'ferrari', 44, 7, '7', 6, 7, 50, 'Finished', 4905831, '0 days 00:00:39.073000', 7, 43, '0 days 00:01:32.600000');
INSERT INTO public.results VALUES (88, 3, 'sainz', 'williams', 55, 8, '8', 4, 6, 50, 'Finished', 4931388, '0 days 00:01:04.630000', 6, 50, '0 days 00:01:32.466000');
INSERT INTO public.results VALUES (89, 3, 'albon', 'williams', 23, 9, '9', 2, 11, 50, 'Finished', 4933273, '0 days 00:01:06.515000', 16, 47, '0 days 00:01:33.477000');
INSERT INTO public.results VALUES (90, 3, 'hadjar', 'rb', 6, 10, '10', 1, 14, 50, 'Finished', 4933849, '0 days 00:01:07.091000', 14, 39, '0 days 00:01:33.257000');
INSERT INTO public.results VALUES (91, 3, 'alonso', 'aston_martin', 14, 11, '11', 0, 13, 50, 'Finished', 4942675, '0 days 00:01:15.917000', 11, 49, '0 days 00:01:33.009000');
INSERT INTO public.results VALUES (92, 3, 'lawson', 'rb', 30, 12, '12', 0, 12, 50, 'Finished', 4945209, '0 days 00:01:18.451000', 10, 43, '0 days 00:01:32.998000');
INSERT INTO public.results VALUES (93, 3, 'bearman', 'haas', 87, 13, '13', 0, 15, 50, 'Finished', 4945952, '0 days 00:01:19.194000', 13, 50, '0 days 00:01:33.238000');
INSERT INTO public.results VALUES (94, 3, 'ocon', 'haas', 31, 14, '14', 0, 19, 50, 'Finished', 4966481, '0 days 00:01:39.723000', 17, 47, '0 days 00:01:34.309000');
INSERT INTO public.results VALUES (95, 3, 'hulkenberg', 'sauber', 27, 15, '15', 0, 18, 49, 'Lapped', 4871367, '0 days 00:00:04.609000', 15, 39, '0 days 00:01:33.446000');
INSERT INTO public.results VALUES (96, 3, 'stroll', 'aston_martin', 18, 16, '16', 0, 16, 49, 'Lapped', 4872285, '0 days 00:00:05.527000', 8, 44, '0 days 00:01:32.745000');
INSERT INTO public.results VALUES (97, 3, 'doohan', 'alpine', 7, 17, '17', 0, 17, 49, 'Lapped', 4886022, '0 days 00:00:19.264000', 12, 48, '0 days 00:01:33.150000');
INSERT INTO public.results VALUES (98, 3, 'bortoleto', 'sauber', 5, 18, '18', 0, 20, 49, 'Lapped', 4886064, '0 days 00:00:19.306000', 18, 39, '0 days 00:01:34.447000');
INSERT INTO public.results VALUES (99, 3, 'tsunoda', 'red_bull', 22, 19, 'R', 0, 8, 1, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (100, 3, 'gasly', 'alpine', 10, 20, 'R', 0, 9, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (101, 4, 'piastri', 'mclaren', 81, 1, '1', 25, 4, 57, 'Finished', 5331587, '0 days 01:28:51.587000', 2, 35, '0 days 00:01:29.822000');
INSERT INTO public.results VALUES (102, 4, 'norris', 'mclaren', 4, 2, '2', 18, 2, 57, 'Finished', 5336217, '0 days 00:00:04.630000', 1, 36, '0 days 00:01:29.746000');
INSERT INTO public.results VALUES (103, 4, 'russell', 'mercedes', 63, 3, '3', 15, 5, 57, 'Finished', 5369231, '0 days 00:00:37.644000', 3, 31, '0 days 00:01:30.318000');
INSERT INTO public.results VALUES (104, 4, 'max_verstappen', 'red_bull', 1, 4, '4', 12, 1, 57, 'Finished', 5371543, '0 days 00:00:39.956000', 5, 41, '0 days 00:01:30.466000');
INSERT INTO public.results VALUES (105, 4, 'albon', 'williams', 23, 5, '5', 10, 7, 57, 'Finished', 5379654, '0 days 00:00:48.067000', 6, 55, '0 days 00:01:30.482000');
INSERT INTO public.results VALUES (106, 4, 'antonelli', 'mercedes', 12, 6, '6', 8, 3, 57, 'Finished', 5387089, '0 days 00:00:55.502000', 9, 27, '0 days 00:01:30.795000');
INSERT INTO public.results VALUES (107, 4, 'leclerc', 'ferrari', 16, 7, '7', 6, 8, 57, 'Finished', 5388623, '0 days 00:00:57.036000', 4, 35, '0 days 00:01:30.461000');
INSERT INTO public.results VALUES (108, 4, 'hamilton', 'ferrari', 44, 8, '8', 4, 12, 57, 'Finished', 5391773, '0 days 00:01:00.186000', 7, 35, '0 days 00:01:30.562000');
INSERT INTO public.results VALUES (109, 4, 'sainz', 'williams', 55, 9, '9', 2, 6, 57, 'Finished', 5392164, '0 days 00:01:00.577000', 8, 35, '0 days 00:01:30.703000');
INSERT INTO public.results VALUES (110, 4, 'tsunoda', 'red_bull', 22, 10, '10', 1, 10, 57, 'Finished', 5406021, '0 days 00:01:14.434000', 10, 55, '0 days 00:01:30.964000');
INSERT INTO public.results VALUES (111, 4, 'hadjar', 'rb', 6, 11, '11', 0, 11, 57, 'Finished', 5406189, '0 days 00:01:14.602000', 11, 51, '0 days 00:01:30.971000');
INSERT INTO public.results VALUES (112, 4, 'ocon', 'haas', 31, 12, '12', 0, 9, 57, 'Finished', 5413593, '0 days 00:01:22.006000', 13, 30, '0 days 00:01:31.122000');
INSERT INTO public.results VALUES (113, 4, 'gasly', 'alpine', 10, 13, '13', 0, 20, 57, 'Finished', 5422032, '0 days 00:01:30.445000', 14, 35, '0 days 00:01:31.159000');
INSERT INTO public.results VALUES (114, 4, 'hulkenberg', 'sauber', 27, 14, '14', 0, 16, 56, 'Lapped', 5332742, '0 days 00:00:01.155000', 12, 43, '0 days 00:01:31.015000');
INSERT INTO public.results VALUES (115, 4, 'alonso', 'aston_martin', 14, 15, '15', 0, 17, 56, 'Lapped', 5352566, '0 days 00:00:20.979000', 15, 38, '0 days 00:01:31.287000');
INSERT INTO public.results VALUES (116, 4, 'stroll', 'aston_martin', 18, 16, '16', 0, 18, 56, 'Lapped', 5356749, '0 days 00:00:25.162000', 16, 50, '0 days 00:01:31.769000');
INSERT INTO public.results VALUES (117, 4, 'lawson', 'rb', 30, 17, 'R', 0, 15, 36, 'Retired', NULL, NULL, 17, 30, '0 days 00:01:31.770000');
INSERT INTO public.results VALUES (118, 4, 'bortoleto', 'sauber', 5, 18, 'R', 0, 13, 30, 'Retired', NULL, NULL, 18, 21, '0 days 00:01:32.328000');
INSERT INTO public.results VALUES (119, 4, 'bearman', 'haas', 87, 19, 'R', 0, 19, 27, 'Retired', NULL, NULL, 19, 24, '0 days 00:01:32.680000');
INSERT INTO public.results VALUES (120, 4, 'doohan', 'alpine', 7, 20, 'R', 0, 14, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (121, 16, 'max_verstappen', 'red_bull', 1, 1, '1', 25, 2, 63, 'Finished', 5493199, '0 days 01:31:33.199000', 1, 58, '0 days 00:01:17.988000');
INSERT INTO public.results VALUES (122, 16, 'norris', 'mclaren', 4, 2, '2', 18, 4, 63, 'Finished', 5499308, '0 days 00:00:06.109000', 4, 63, '0 days 00:01:18.311000');
INSERT INTO public.results VALUES (123, 16, 'piastri', 'mclaren', 81, 3, '3', 15, 1, 63, 'Finished', 5506155, '0 days 00:00:12.956000', 5, 56, '0 days 00:01:18.894000');
INSERT INTO public.results VALUES (124, 16, 'hamilton', 'ferrari', 44, 4, '4', 12, 12, 63, 'Finished', 5507555, '0 days 00:00:14.356000', 2, 61, '0 days 00:01:18.265000');
INSERT INTO public.results VALUES (125, 16, 'albon', 'williams', 23, 5, '5', 10, 7, 63, 'Finished', 5511144, '0 days 00:00:17.945000', 3, 63, '0 days 00:01:18.289000');
INSERT INTO public.results VALUES (126, 16, 'leclerc', 'ferrari', 16, 6, '6', 8, 11, 63, 'Finished', 5513973, '0 days 00:00:20.774000', 6, 56, '0 days 00:01:19.048000');
INSERT INTO public.results VALUES (127, 16, 'russell', 'mercedes', 63, 7, '7', 6, 3, 63, 'Finished', 5515233, '0 days 00:00:22.034000', 9, 55, '0 days 00:01:19.733000');
INSERT INTO public.results VALUES (128, 16, 'sainz', 'williams', 55, 8, '8', 4, 6, 63, 'Finished', 5516097, '0 days 00:00:22.898000', 10, 58, '0 days 00:01:19.836000');
INSERT INTO public.results VALUES (129, 16, 'hadjar', 'rb', 6, 9, '9', 2, 9, 63, 'Finished', 5516785, '0 days 00:00:23.586000', 7, 60, '0 days 00:01:19.473000');
INSERT INTO public.results VALUES (130, 16, 'tsunoda', 'red_bull', 22, 10, '10', 1, 20, 63, 'Finished', 5519645, '0 days 00:00:26.446000', 12, 60, '0 days 00:01:20.039000');
INSERT INTO public.results VALUES (131, 16, 'alonso', 'aston_martin', 14, 11, '11', 0, 5, 63, 'Finished', 5520449, '0 days 00:00:27.250000', 11, 61, '0 days 00:01:19.894000');
INSERT INTO public.results VALUES (132, 16, 'hulkenberg', 'sauber', 27, 12, '12', 0, 17, 63, 'Finished', 5523495, '0 days 00:00:30.296000', 15, 62, '0 days 00:01:20.401000');
INSERT INTO public.results VALUES (133, 16, 'gasly', 'alpine', 10, 13, '13', 0, 10, 63, 'Finished', 5524623, '0 days 00:00:31.424000', 14, 58, '0 days 00:01:20.398000');
INSERT INTO public.results VALUES (134, 16, 'lawson', 'rb', 30, 14, '14', 0, 15, 63, 'Finished', 5525710, '0 days 00:00:32.511000', 16, 60, '0 days 00:01:20.473000');
INSERT INTO public.results VALUES (135, 16, 'stroll', 'aston_martin', 18, 15, '15', 0, 8, 63, 'Finished', 5526192, '0 days 00:00:32.993000', 17, 58, '0 days 00:01:20.501000');
INSERT INTO public.results VALUES (136, 16, 'colapinto', 'alpine', 43, 16, '16', 0, 16, 63, 'Finished', 5526610, '0 days 00:00:33.411000', 13, 57, '0 days 00:01:20.345000');
INSERT INTO public.results VALUES (137, 16, 'bearman', 'haas', 87, 17, '17', 0, 19, 63, 'Finished', 5527007, '0 days 00:00:33.808000', 8, 52, '0 days 00:01:19.521000');
INSERT INTO public.results VALUES (138, 16, 'bortoleto', 'sauber', 5, 18, '18', 0, 14, 63, 'Finished', 5531771, '0 days 00:00:38.572000', 19, 57, '0 days 00:01:20.630000');
INSERT INTO public.results VALUES (139, 16, 'antonelli', 'mercedes', 12, 19, 'R', 0, 13, 44, 'Retired', NULL, NULL, 18, 33, '0 days 00:01:20.620000');
INSERT INTO public.results VALUES (140, 16, 'ocon', 'haas', 31, 20, 'R', 0, 18, 27, 'Retired', NULL, NULL, 20, 3, '0 days 00:01:21.413000');
INSERT INTO public.results VALUES (141, 5, 'norris', 'mclaren', 4, 1, '1', 25, 1, 78, 'Finished', 6033843, '0 days 01:40:33.843000', 1, 78, '0 days 00:01:13.221000');
INSERT INTO public.results VALUES (142, 5, 'leclerc', 'ferrari', 16, 2, '2', 18, 2, 78, 'Finished', 6036974, '0 days 00:00:03.131000', 6, 36, '0 days 00:01:14.055000');
INSERT INTO public.results VALUES (143, 5, 'piastri', 'mclaren', 81, 3, '3', 15, 3, 78, 'Finished', 6037501, '0 days 00:00:03.658000', 4, 60, '0 days 00:01:13.745000');
INSERT INTO public.results VALUES (144, 5, 'max_verstappen', 'red_bull', 1, 4, '4', 12, 4, 78, 'Finished', 6054415, '0 days 00:00:20.572000', 8, 45, '0 days 00:01:14.230000');
INSERT INTO public.results VALUES (145, 5, 'hamilton', 'ferrari', 44, 5, '5', 10, 7, 78, 'Finished', 6085230, '0 days 00:00:51.387000', 7, 73, '0 days 00:01:14.090000');
INSERT INTO public.results VALUES (146, 5, 'hadjar', 'rb', 6, 6, '6', 8, 5, 77, 'Lapped', 6098925, '0 days 00:01:05.082000', 19, 16, '0 days 00:01:15.981000');
INSERT INTO public.results VALUES (147, 5, 'ocon', 'haas', 31, 7, '7', 6, 8, 77, 'Lapped', 6099872, '0 days 00:01:06.029000', 14, 34, '0 days 00:01:15.157000');
INSERT INTO public.results VALUES (148, 5, 'lawson', 'rb', 30, 8, '8', 4, 9, 77, 'Lapped', 6100589, '0 days 00:01:06.746000', 17, 54, '0 days 00:01:15.321000');
INSERT INTO public.results VALUES (149, 5, 'albon', 'williams', 23, 9, '9', 2, 10, 76, 'Lapped', 6045712, '0 days 00:00:11.869000', 9, 74, '0 days 00:01:14.597000');
INSERT INTO public.results VALUES (150, 5, 'sainz', 'williams', 55, 10, '10', 1, 11, 76, 'Lapped', 6049075, '0 days 00:00:15.232000', 5, 68, '0 days 00:01:13.988000');
INSERT INTO public.results VALUES (151, 5, 'russell', 'mercedes', 63, 11, '11', 0, 14, 76, 'Lapped', 6067687, '0 days 00:00:33.844000', 2, 74, '0 days 00:01:13.405000');
INSERT INTO public.results VALUES (152, 5, 'bearman', 'haas', 87, 12, '12', 0, 20, 76, 'Lapped', 6088536, '0 days 00:00:54.693000', 10, 6, '0 days 00:01:14.855000');
INSERT INTO public.results VALUES (153, 5, 'colapinto', 'alpine', 43, 13, '13', 0, 18, 76, 'Lapped', 6090957, '0 days 00:00:57.114000', 16, 30, '0 days 00:01:15.298000');
INSERT INTO public.results VALUES (154, 5, 'bortoleto', 'sauber', 5, 14, '14', 0, 16, 76, 'Lapped', 6102267, '0 days 00:01:08.424000', 12, 37, '0 days 00:01:14.884000');
INSERT INTO public.results VALUES (155, 5, 'stroll', 'aston_martin', 18, 15, '15', 0, 19, 76, 'Lapped', 6104238, '0 days 00:01:10.395000', 11, 67, '0 days 00:01:14.877000');
INSERT INTO public.results VALUES (156, 5, 'hulkenberg', 'sauber', 27, 16, '16', 0, 13, 76, 'Lapped', 6105387, '0 days 00:01:11.544000', 15, 47, '0 days 00:01:15.223000');
INSERT INTO public.results VALUES (157, 5, 'tsunoda', 'red_bull', 22, 17, '17', 0, 12, 76, 'Lapped', 6105692, '0 days 00:01:11.849000', 13, 75, '0 days 00:01:14.913000');
INSERT INTO public.results VALUES (158, 5, 'antonelli', 'mercedes', 12, 18, '18', 0, 15, 75, 'Lapped', 6042252, '0 days 00:00:08.409000', 3, 74, '0 days 00:01:13.518000');
INSERT INTO public.results VALUES (159, 5, 'alonso', 'aston_martin', 14, 19, 'R', 0, 6, 36, 'Retired', NULL, NULL, 18, 15, '0 days 00:01:15.593000');
INSERT INTO public.results VALUES (160, 5, 'gasly', 'alpine', 10, 20, 'R', 0, 17, 7, 'Retired', NULL, NULL, 20, 6, '0 days 00:01:18.054000');
INSERT INTO public.results VALUES (161, 6, 'piastri', 'mclaren', 81, 1, '1', 25, 1, 66, 'Finished', 5577375, '0 days 01:32:57.375000', 1, 61, '0 days 00:01:15.743000');
INSERT INTO public.results VALUES (162, 6, 'norris', 'mclaren', 4, 2, '2', 18, 2, 66, 'Finished', 5579846, '0 days 00:00:02.471000', 2, 61, '0 days 00:01:16.187000');
INSERT INTO public.results VALUES (163, 6, 'leclerc', 'ferrari', 16, 3, '3', 15, 7, 66, 'Finished', 5587830, '0 days 00:00:10.455000', 5, 62, '0 days 00:01:17.259000');
INSERT INTO public.results VALUES (164, 6, 'russell', 'mercedes', 63, 4, '4', 12, 4, 66, 'Finished', 5588734, '0 days 00:00:11.359000', 4, 62, '0 days 00:01:17.244000');
INSERT INTO public.results VALUES (165, 6, 'hulkenberg', 'sauber', 27, 5, '5', 10, 15, 66, 'Finished', 5591023, '0 days 00:00:13.648000', 6, 63, '0 days 00:01:17.575000');
INSERT INTO public.results VALUES (166, 6, 'hamilton', 'ferrari', 44, 6, '6', 8, 5, 66, 'Finished', 5592883, '0 days 00:00:15.508000', 7, 62, '0 days 00:01:17.706000');
INSERT INTO public.results VALUES (167, 6, 'hadjar', 'rb', 6, 7, '7', 6, 9, 66, 'Finished', 5593397, '0 days 00:00:16.022000', 8, 63, '0 days 00:01:17.770000');
INSERT INTO public.results VALUES (168, 6, 'gasly', 'alpine', 10, 8, '8', 4, 8, 66, 'Finished', 5595257, '0 days 00:00:17.882000', 9, 63, '0 days 00:01:17.896000');
INSERT INTO public.results VALUES (169, 6, 'alonso', 'aston_martin', 14, 9, '9', 2, 10, 66, 'Finished', 5598939, '0 days 00:00:21.564000', 11, 66, '0 days 00:01:18.128000');
INSERT INTO public.results VALUES (170, 6, 'max_verstappen', 'red_bull', 1, 10, '10', 1, 3, 66, 'Finished', 5599201, '0 days 00:00:21.826000', 3, 62, '0 days 00:01:17.019000');
INSERT INTO public.results VALUES (171, 6, 'lawson', 'rb', 30, 11, '11', 0, 13, 66, 'Finished', 5602907, '0 days 00:00:25.532000', 18, 62, '0 days 00:01:19.424000');
INSERT INTO public.results VALUES (172, 6, 'bortoleto', 'sauber', 5, 12, '12', 0, 12, 66, 'Finished', 5603371, '0 days 00:00:25.996000', 13, 51, '0 days 00:01:18.297000');
INSERT INTO public.results VALUES (173, 6, 'tsunoda', 'red_bull', 22, 13, '13', 0, 19, 66, 'Finished', 5606197, '0 days 00:00:28.822000', 10, 46, '0 days 00:01:17.998000');
INSERT INTO public.results VALUES (174, 6, 'sainz', 'williams', 55, 14, '14', 0, 17, 66, 'Finished', 5606684, '0 days 00:00:29.309000', 17, 65, '0 days 00:01:19.317000');
INSERT INTO public.results VALUES (175, 6, 'colapinto', 'alpine', 43, 15, '15', 0, 18, 66, 'Finished', 5608756, '0 days 00:00:31.381000', 14, 41, '0 days 00:01:18.353000');
INSERT INTO public.results VALUES (176, 6, 'ocon', 'haas', 31, 16, '16', 0, 16, 66, 'Finished', 5609572, '0 days 00:00:32.197000', 15, 46, '0 days 00:01:18.624000');
INSERT INTO public.results VALUES (177, 6, 'bearman', 'haas', 87, 17, '17', 0, 14, 66, 'Finished', 5614440, '0 days 00:00:37.065000', 16, 63, '0 days 00:01:18.907000');
INSERT INTO public.results VALUES (178, 6, 'antonelli', 'mercedes', 12, 18, 'R', 0, 6, 53, 'Retired', NULL, NULL, 12, 52, '0 days 00:01:18.255000');
INSERT INTO public.results VALUES (179, 6, 'albon', 'williams', 23, 19, 'R', 0, 11, 27, 'Retired', NULL, NULL, 19, 9, '0 days 00:01:20.508000');
INSERT INTO public.results VALUES (180, 17, 'russell', 'mercedes', 63, 1, '1', 25, 1, 70, 'Finished', 5512688, '0 days 01:31:52.688000', 1, 63, '0 days 00:01:14.119000');
INSERT INTO public.results VALUES (181, 17, 'max_verstappen', 'red_bull', 1, 2, '2', 18, 2, 70, 'Finished', 5512916, '0 days 00:00:00.228000', 5, 62, '0 days 00:01:14.287000');
INSERT INTO public.results VALUES (182, 17, 'antonelli', 'mercedes', 12, 3, '3', 15, 4, 70, 'Finished', 5513702, '0 days 00:00:01.014000', 7, 60, '0 days 00:01:14.455000');
INSERT INTO public.results VALUES (183, 17, 'piastri', 'mclaren', 81, 4, '4', 12, 3, 70, 'Finished', 5514797, '0 days 00:00:02.109000', 3, 64, '0 days 00:01:14.255000');
INSERT INTO public.results VALUES (184, 17, 'leclerc', 'ferrari', 16, 5, '5', 10, 8, 70, 'Finished', 5516130, '0 days 00:00:03.442000', 4, 57, '0 days 00:01:14.261000');
INSERT INTO public.results VALUES (185, 17, 'hamilton', 'ferrari', 44, 6, '6', 8, 5, 70, 'Finished', 5523401, '0 days 00:00:10.713000', 9, 64, '0 days 00:01:14.805000');
INSERT INTO public.results VALUES (186, 17, 'alonso', 'aston_martin', 14, 7, '7', 6, 6, 70, 'Finished', 5523660, '0 days 00:00:10.972000', 12, 58, '0 days 00:01:15.024000');
INSERT INTO public.results VALUES (187, 17, 'hulkenberg', 'sauber', 27, 8, '8', 4, 11, 70, 'Finished', 5528052, '0 days 00:00:15.364000', 14, 65, '0 days 00:01:15.372000');
INSERT INTO public.results VALUES (188, 17, 'ocon', 'haas', 31, 9, '9', 2, 14, 69, 'Lapped', 5514161, '0 days 00:00:01.473000', 8, 61, '0 days 00:01:14.593000');
INSERT INTO public.results VALUES (189, 17, 'sainz', 'williams', 55, 10, '10', 1, 16, 69, 'Lapped', 5514574, '0 days 00:00:01.886000', 6, 59, '0 days 00:01:14.389000');
INSERT INTO public.results VALUES (190, 17, 'bearman', 'haas', 87, 11, '11', 0, 13, 69, 'Lapped', 5516405, '0 days 00:00:03.717000', 15, 62, '0 days 00:01:15.397000');
INSERT INTO public.results VALUES (191, 17, 'tsunoda', 'red_bull', 22, 12, '12', 0, 18, 69, 'Lapped', 5518144, '0 days 00:00:05.456000', 13, 59, '0 days 00:01:15.358000');
INSERT INTO public.results VALUES (192, 17, 'colapinto', 'alpine', 43, 13, '13', 0, 10, 69, 'Lapped', 5519706, '0 days 00:00:07.018000', 17, 53, '0 days 00:01:16.076000');
INSERT INTO public.results VALUES (193, 17, 'bortoleto', 'sauber', 5, 14, '14', 0, 15, 69, 'Lapped', 5520567, '0 days 00:00:07.879000', 16, 56, '0 days 00:01:15.414000');
INSERT INTO public.results VALUES (194, 17, 'gasly', 'alpine', 10, 15, '15', 0, 20, 69, 'Lapped', 5520638, '0 days 00:00:07.950000', 11, 63, '0 days 00:01:14.993000');
INSERT INTO public.results VALUES (195, 17, 'hadjar', 'rb', 6, 16, '16', 0, 12, 69, 'Lapped', 5521425, '0 days 00:00:08.737000', 19, 51, '0 days 00:01:16.292000');
INSERT INTO public.results VALUES (196, 17, 'stroll', 'aston_martin', 18, 17, '17', 0, 17, 69, 'Lapped', 5521751, '0 days 00:00:09.063000', 10, 57, '0 days 00:01:14.902000');
INSERT INTO public.results VALUES (197, 17, 'norris', 'mclaren', 4, 18, '18', 0, 7, 66, 'Retired', 5042470, NULL, 2, 65, '0 days 00:01:14.229000');
INSERT INTO public.results VALUES (198, 17, 'lawson', 'rb', 30, 19, 'R', 0, 19, 53, 'Retired', NULL, NULL, 20, 52, '0 days 00:01:16.320000');
INSERT INTO public.results VALUES (199, 17, 'albon', 'williams', 23, 20, 'R', 0, 9, 46, 'Retired', NULL, NULL, 18, 31, '0 days 00:01:16.197000');
INSERT INTO public.results VALUES (200, 18, 'norris', 'mclaren', 4, 1, '1', 25, 1, 70, 'Finished', 5027693, '0 days 01:23:47.693000', 2, 61, '0 days 00:01:08.272000');
INSERT INTO public.results VALUES (201, 18, 'piastri', 'mclaren', 81, 2, '2', 18, 3, 70, 'Finished', 5030388, '0 days 00:00:02.695000', 1, 59, '0 days 00:01:07.924000');
INSERT INTO public.results VALUES (202, 18, 'leclerc', 'ferrari', 16, 3, '3', 15, 2, 70, 'Finished', 5047513, '0 days 00:00:19.820000', 4, 56, '0 days 00:01:08.765000');
INSERT INTO public.results VALUES (203, 18, 'hamilton', 'ferrari', 44, 4, '4', 12, 4, 70, 'Finished', 5056713, '0 days 00:00:29.020000', 3, 53, '0 days 00:01:08.628000');
INSERT INTO public.results VALUES (204, 18, 'russell', 'mercedes', 63, 5, '5', 10, 5, 70, 'Finished', 5090089, '0 days 00:01:02.396000', 7, 47, '0 days 00:01:09.372000');
INSERT INTO public.results VALUES (205, 18, 'lawson', 'rb', 30, 6, '6', 8, 6, 70, 'Finished', 5095447, '0 days 00:01:07.754000', 14, 58, '0 days 00:01:09.977000');
INSERT INTO public.results VALUES (206, 18, 'alonso', 'aston_martin', 14, 7, '7', 6, 11, 69, 'Lapped', 5029130, '0 days 00:00:01.437000', 12, 39, '0 days 00:01:09.935000');
INSERT INTO public.results VALUES (207, 18, 'bortoleto', 'sauber', 5, 8, '8', 4, 8, 69, 'Lapped', 5029645, '0 days 00:00:01.952000', 6, 60, '0 days 00:01:09.247000');
INSERT INTO public.results VALUES (208, 18, 'hulkenberg', 'sauber', 27, 9, '9', 2, 20, 69, 'Lapped', 5035413, '0 days 00:00:07.720000', 8, 57, '0 days 00:01:09.459000');
INSERT INTO public.results VALUES (209, 18, 'ocon', 'haas', 31, 10, '10', 1, 17, 69, 'Lapped', 5037679, '0 days 00:00:09.986000', 9, 55, '0 days 00:01:09.550000');
INSERT INTO public.results VALUES (210, 18, 'bearman', 'haas', 87, 11, '11', 0, 15, 69, 'Lapped', 5052547, '0 days 00:00:24.854000', 13, 42, '0 days 00:01:09.960000');
INSERT INTO public.results VALUES (211, 18, 'hadjar', 'rb', 6, 12, '12', 0, 13, 69, 'Lapped', 5055650, '0 days 00:00:27.957000', 16, 40, '0 days 00:01:10.204000');
INSERT INTO public.results VALUES (212, 18, 'gasly', 'alpine', 10, 13, '13', 0, 10, 69, 'Lapped', 5060748, '0 days 00:00:33.055000', 15, 46, '0 days 00:01:10.151000');
INSERT INTO public.results VALUES (213, 18, 'stroll', 'aston_martin', 18, 14, '14', 0, 16, 69, 'Lapped', 5062155, '0 days 00:00:34.462000', 5, 55, '0 days 00:01:09.214000');
INSERT INTO public.results VALUES (214, 18, 'colapinto', 'alpine', 43, 15, '15', 0, 14, 69, 'Lapped', 5070385, '0 days 00:00:42.692000', 10, 44, '0 days 00:01:09.621000');
INSERT INTO public.results VALUES (215, 18, 'tsunoda', 'red_bull', 22, 16, '16', 0, 18, 68, 'Lapped', 5030672, '0 days 00:00:02.979000', 11, 62, '0 days 00:01:09.802000');
INSERT INTO public.results VALUES (216, 18, 'albon', 'williams', 23, 17, 'R', 0, 12, 15, 'Retired', NULL, NULL, 17, 9, '0 days 00:01:10.641000');
INSERT INTO public.results VALUES (217, 18, 'max_verstappen', 'red_bull', 1, 18, 'R', 0, 7, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (218, 18, 'antonelli', 'mercedes', 12, 19, 'R', 0, 9, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (219, 18, 'sainz', 'williams', 55, 20, 'W', 0, 19, 0, 'Did not start', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (220, 7, 'norris', 'mclaren', 4, 1, '1', 25, 3, 52, 'Finished', 5835735, '0 days 01:37:15.735000', 2, 48, '0 days 00:01:29.734000');
INSERT INTO public.results VALUES (221, 7, 'piastri', 'mclaren', 81, 2, '2', 18, 2, 52, 'Finished', 5842547, '0 days 00:00:06.812000', 1, 51, '0 days 00:01:29.337000');
INSERT INTO public.results VALUES (222, 7, 'hulkenberg', 'sauber', 27, 3, '3', 15, 19, 52, 'Finished', 5870477, '0 days 00:00:34.742000', 14, 51, '0 days 00:01:30.933000');
INSERT INTO public.results VALUES (223, 7, 'hamilton', 'ferrari', 44, 4, '4', 12, 5, 52, 'Finished', 5875547, '0 days 00:00:39.812000', 3, 49, '0 days 00:01:30.016000');
INSERT INTO public.results VALUES (224, 7, 'max_verstappen', 'red_bull', 1, 5, '5', 10, 1, 52, 'Finished', 5892516, '0 days 00:00:56.781000', 5, 49, '0 days 00:01:30.179000');
INSERT INTO public.results VALUES (225, 7, 'gasly', 'alpine', 10, 6, '6', 8, 8, 52, 'Finished', 5895592, '0 days 00:00:59.857000', 8, 48, '0 days 00:01:30.751000');
INSERT INTO public.results VALUES (226, 7, 'stroll', 'aston_martin', 18, 7, '7', 6, 17, 52, 'Finished', 5896338, '0 days 00:01:00.603000', 15, 50, '0 days 00:01:32.088000');
INSERT INTO public.results VALUES (227, 7, 'albon', 'williams', 23, 8, '8', 4, 13, 52, 'Finished', 5899870, '0 days 00:01:04.135000', 4, 50, '0 days 00:01:30.047000');
INSERT INTO public.results VALUES (228, 7, 'alonso', 'aston_martin', 14, 9, '9', 2, 7, 52, 'Finished', 5901593, '0 days 00:01:05.858000', 6, 49, '0 days 00:01:30.353000');
INSERT INTO public.results VALUES (229, 7, 'russell', 'mercedes', 63, 10, '10', 1, 4, 52, 'Finished', 5906409, '0 days 00:01:10.674000', 11, 51, '0 days 00:01:30.869000');
INSERT INTO public.results VALUES (230, 7, 'bearman', 'haas', 87, 11, '11', 0, 18, 52, 'Finished', 5907830, '0 days 00:01:12.095000', 13, 50, '0 days 00:01:30.921000');
INSERT INTO public.results VALUES (231, 7, 'sainz', 'williams', 55, 12, '12', 0, 9, 52, 'Finished', 5912327, '0 days 00:01:16.592000', 7, 52, '0 days 00:01:30.645000');
INSERT INTO public.results VALUES (232, 7, 'ocon', 'haas', 31, 13, '13', 0, 14, 52, 'Finished', 5913036, '0 days 00:01:17.301000', 9, 52, '0 days 00:01:30.818000');
INSERT INTO public.results VALUES (233, 7, 'leclerc', 'ferrari', 16, 14, '14', 0, 6, 52, 'Finished', 5920212, '0 days 00:01:24.477000', 10, 50, '0 days 00:01:30.819000');
INSERT INTO public.results VALUES (234, 7, 'tsunoda', 'red_bull', 22, 15, '15', 0, 11, 51, 'Lapped', 5867985, '0 days 00:00:32.250000', 12, 49, '0 days 00:01:30.873000');
INSERT INTO public.results VALUES (235, 7, 'antonelli', 'mercedes', 12, 16, 'R', 0, 10, 23, 'Retired', NULL, NULL, 17, 8, '0 days 00:01:45.576000');
INSERT INTO public.results VALUES (236, 7, 'hadjar', 'rb', 6, 17, 'R', 0, 12, 17, 'Retired', NULL, NULL, 16, 9, '0 days 00:01:41.705000');
INSERT INTO public.results VALUES (237, 7, 'bortoleto', 'sauber', 5, 18, 'R', 0, 16, 3, 'Retired', NULL, NULL, 18, 3, '0 days 00:02:16.121000');
INSERT INTO public.results VALUES (238, 7, 'lawson', 'rb', 30, 19, 'R', 0, 15, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (239, 7, 'colapinto', 'alpine', 43, 20, 'W', 0, 20, 0, 'Did not start', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (240, 8, 'piastri', 'mclaren', 81, 1, '1', 25, 2, 44, 'Finished', 5122601, '0 days 01:25:22.601000', 4, 43, '0 days 00:01:45.706000');
INSERT INTO public.results VALUES (241, 8, 'norris', 'mclaren', 4, 2, '2', 18, 1, 44, 'Finished', 5126016, '0 days 00:00:03.415000', 3, 42, '0 days 00:01:45.257000');
INSERT INTO public.results VALUES (242, 8, 'leclerc', 'ferrari', 16, 3, '3', 15, 3, 44, 'Finished', 5142786, '0 days 00:00:20.185000', 9, 40, '0 days 00:01:46.174000');
INSERT INTO public.results VALUES (243, 8, 'max_verstappen', 'red_bull', 1, 4, '4', 12, 4, 44, 'Finished', 5144332, '0 days 00:00:21.731000', 7, 40, '0 days 00:01:46.096000');
INSERT INTO public.results VALUES (244, 8, 'russell', 'mercedes', 63, 5, '5', 10, 6, 44, 'Finished', 5157464, '0 days 00:00:34.863000', 11, 43, '0 days 00:01:46.566000');
INSERT INTO public.results VALUES (245, 8, 'albon', 'williams', 23, 6, '6', 8, 5, 44, 'Finished', 5162527, '0 days 00:00:39.926000', 15, 38, '0 days 00:01:46.813000');
INSERT INTO public.results VALUES (246, 8, 'hamilton', 'ferrari', 44, 7, '7', 6, 18, 44, 'Finished', 5163280, '0 days 00:00:40.679000', 10, 43, '0 days 00:01:46.534000');
INSERT INTO public.results VALUES (247, 8, 'lawson', 'rb', 30, 8, '8', 4, 9, 44, 'Finished', 5174634, '0 days 00:00:52.033000', 12, 38, '0 days 00:01:46.649000');
INSERT INTO public.results VALUES (248, 8, 'bortoleto', 'sauber', 5, 9, '9', 2, 10, 44, 'Finished', 5179035, '0 days 00:00:56.434000', 16, 41, '0 days 00:01:46.966000');
INSERT INTO public.results VALUES (249, 8, 'gasly', 'alpine', 10, 10, '10', 1, 13, 44, 'Finished', 5195315, '0 days 00:01:12.714000', 17, 42, '0 days 00:01:47.177000');
INSERT INTO public.results VALUES (250, 8, 'bearman', 'haas', 87, 11, '11', 0, 12, 44, 'Finished', 5195746, '0 days 00:01:13.145000', 13, 43, '0 days 00:01:46.709000');
INSERT INTO public.results VALUES (251, 8, 'hulkenberg', 'sauber', 27, 12, '12', 0, 14, 44, 'Finished', 5196229, '0 days 00:01:13.628000', 2, 39, '0 days 00:01:45.068000');
INSERT INTO public.results VALUES (252, 8, 'tsunoda', 'red_bull', 22, 13, '13', 0, 7, 44, 'Finished', 5197996, '0 days 00:01:15.395000', 19, 42, '0 days 00:01:47.241000');
INSERT INTO public.results VALUES (253, 8, 'stroll', 'aston_martin', 18, 14, '14', 0, 16, 44, 'Finished', 5202432, '0 days 00:01:19.831000', 18, 38, '0 days 00:01:47.212000');
INSERT INTO public.results VALUES (254, 8, 'ocon', 'haas', 31, 15, '15', 0, 11, 44, 'Finished', 5208664, '0 days 00:01:26.063000', 14, 44, '0 days 00:01:46.744000');
INSERT INTO public.results VALUES (255, 8, 'antonelli', 'mercedes', 12, 16, '16', 0, 19, 44, 'Finished', 5209322, '0 days 00:01:26.721000', 1, 32, '0 days 00:01:44.861000');
INSERT INTO public.results VALUES (256, 8, 'alonso', 'aston_martin', 14, 17, '17', 0, 20, 44, 'Finished', 5210525, '0 days 00:01:27.924000', 5, 32, '0 days 00:01:45.849000');
INSERT INTO public.results VALUES (257, 8, 'sainz', 'williams', 55, 18, '18', 0, 17, 44, 'Finished', 5214625, '0 days 00:01:32.024000', 6, 30, '0 days 00:01:46.073000');
INSERT INTO public.results VALUES (258, 8, 'colapinto', 'alpine', 43, 19, '19', 0, 15, 44, 'Finished', 5217851, '0 days 00:01:35.250000', 8, 30, '0 days 00:01:46.104000');
INSERT INTO public.results VALUES (259, 8, 'hadjar', 'rb', 6, 20, '20', 0, 8, 43, 'Lapped', 5135543, '0 days 00:00:12.942000', 20, 43, '0 days 00:01:47.667000');
INSERT INTO public.results VALUES (260, 19, 'norris', 'mclaren', 4, 1, '1', 25, 3, 70, 'Finished', 5721231, '0 days 01:35:21.231000', 5, 57, '0 days 00:01:19.918000');
INSERT INTO public.results VALUES (261, 19, 'piastri', 'mclaren', 81, 2, '2', 18, 2, 70, 'Finished', 5721929, '0 days 00:00:00.698000', 2, 56, '0 days 00:01:19.412000');
INSERT INTO public.results VALUES (262, 19, 'russell', 'mercedes', 63, 3, '3', 15, 4, 70, 'Finished', 5743147, '0 days 00:00:21.916000', 1, 45, '0 days 00:01:19.409000');
INSERT INTO public.results VALUES (263, 19, 'leclerc', 'ferrari', 16, 4, '4', 12, 1, 70, 'Finished', 5763791, '0 days 00:00:42.560000', 9, 47, '0 days 00:01:20.440000');
INSERT INTO public.results VALUES (264, 19, 'alonso', 'aston_martin', 14, 5, '5', 10, 5, 70, 'Finished', 5780271, '0 days 00:00:59.040000', 8, 54, '0 days 00:01:20.113000');
INSERT INTO public.results VALUES (265, 19, 'bortoleto', 'sauber', 5, 6, '6', 8, 7, 70, 'Finished', 5787400, '0 days 00:01:06.169000', 11, 48, '0 days 00:01:20.705000');
INSERT INTO public.results VALUES (266, 19, 'stroll', 'aston_martin', 18, 7, '7', 6, 6, 70, 'Finished', 5789405, '0 days 00:01:08.174000', 12, 55, '0 days 00:01:20.708000');
INSERT INTO public.results VALUES (267, 19, 'lawson', 'rb', 30, 8, '8', 4, 9, 70, 'Finished', 5790682, '0 days 00:01:09.451000', 10, 56, '0 days 00:01:20.457000');
INSERT INTO public.results VALUES (268, 19, 'max_verstappen', 'red_bull', 1, 9, '9', 2, 8, 70, 'Finished', 5793876, '0 days 00:01:12.645000', 3, 50, '0 days 00:01:19.576000');
INSERT INTO public.results VALUES (269, 19, 'antonelli', 'mercedes', 12, 10, '10', 1, 15, 69, 'Lapped', 5728880, '0 days 00:00:07.649000', 13, 54, '0 days 00:01:20.745000');
INSERT INTO public.results VALUES (270, 19, 'hadjar', 'rb', 6, 11, '11', 0, 10, 69, 'Lapped', 5729731, '0 days 00:00:08.500000', 15, 48, '0 days 00:01:20.802000');
INSERT INTO public.results VALUES (271, 19, 'hamilton', 'ferrari', 44, 12, '12', 0, 12, 69, 'Lapped', 5731092, '0 days 00:00:09.861000', 7, 55, '0 days 00:01:20.022000');
INSERT INTO public.results VALUES (272, 19, 'hulkenberg', 'sauber', 27, 13, '13', 0, 18, 69, 'Lapped', 5752499, '0 days 00:00:31.268000', 6, 67, '0 days 00:01:20.013000');
INSERT INTO public.results VALUES (273, 19, 'sainz', 'williams', 55, 14, '14', 0, 13, 69, 'Lapped', 5754557, '0 days 00:00:33.326000', 4, 53, '0 days 00:01:19.790000');
INSERT INTO public.results VALUES (274, 19, 'albon', 'williams', 23, 15, '15', 0, 19, 69, 'Lapped', 5759342, '0 days 00:00:38.111000', 14, 49, '0 days 00:01:20.779000');
INSERT INTO public.results VALUES (275, 19, 'ocon', 'haas', 31, 16, '16', 0, 17, 69, 'Lapped', 5766489, '0 days 00:00:45.258000', 19, 17, '0 days 00:01:21.916000');
INSERT INTO public.results VALUES (276, 19, 'tsunoda', 'red_bull', 22, 17, '17', 0, 20, 69, 'Lapped', 5768174, '0 days 00:00:46.943000', 17, 46, '0 days 00:01:21.180000');
INSERT INTO public.results VALUES (277, 19, 'colapinto', 'alpine', 43, 18, '18', 0, 14, 69, 'Lapped', 5768601, '0 days 00:00:47.370000', 16, 37, '0 days 00:01:20.827000');
INSERT INTO public.results VALUES (278, 19, 'gasly', 'alpine', 10, 19, '19', 0, 16, 69, 'Lapped', 5777575, '0 days 00:00:56.344000', 18, 46, '0 days 00:01:21.433000');
INSERT INTO public.results VALUES (279, 19, 'bearman', 'haas', 87, 20, 'R', 0, 11, 48, 'Retired', NULL, NULL, 20, 37, '0 days 00:01:21.989000');
INSERT INTO public.results VALUES (280, 9, 'piastri', 'mclaren', 81, 1, '1', 25, 1, 72, 'Finished', 5909849, '0 days 01:38:29.849000', 1, 60, '0 days 00:01:12.271000');
INSERT INTO public.results VALUES (281, 9, 'max_verstappen', 'red_bull', 1, 2, '2', 18, 3, 72, 'Finished', 5911120, '0 days 00:00:01.271000', 3, 70, '0 days 00:01:12.921000');
INSERT INTO public.results VALUES (282, 9, 'hadjar', 'rb', 6, 3, '3', 15, 4, 72, 'Finished', 5913082, '0 days 00:00:03.233000', 5, 70, '0 days 00:01:13.327000');
INSERT INTO public.results VALUES (283, 9, 'russell', 'mercedes', 63, 4, '4', 12, 5, 72, 'Finished', 5915503, '0 days 00:00:05.654000', 9, 70, '0 days 00:01:13.728000');
INSERT INTO public.results VALUES (284, 9, 'albon', 'williams', 23, 5, '5', 10, 15, 72, 'Finished', 5916176, '0 days 00:00:06.327000', 7, 70, '0 days 00:01:13.687000');
INSERT INTO public.results VALUES (285, 9, 'bearman', 'haas', 87, 6, '6', 8, 20, 72, 'Finished', 5918893, '0 days 00:00:09.044000', 13, 70, '0 days 00:01:13.950000');
INSERT INTO public.results VALUES (286, 9, 'stroll', 'aston_martin', 18, 7, '7', 6, 19, 72, 'Finished', 5919346, '0 days 00:00:09.497000', 11, 70, '0 days 00:01:13.822000');
INSERT INTO public.results VALUES (287, 9, 'alonso', 'aston_martin', 14, 8, '8', 4, 10, 72, 'Finished', 5921558, '0 days 00:00:11.709000', 8, 42, '0 days 00:01:13.719000');
INSERT INTO public.results VALUES (288, 9, 'tsunoda', 'red_bull', 22, 9, '9', 2, 12, 72, 'Finished', 5923446, '0 days 00:00:13.597000', 16, 71, '0 days 00:01:14.354000');
INSERT INTO public.results VALUES (289, 9, 'ocon', 'haas', 31, 10, '10', 1, 18, 72, 'Finished', 5923912, '0 days 00:00:14.063000', 14, 71, '0 days 00:01:13.986000');
INSERT INTO public.results VALUES (290, 9, 'colapinto', 'alpine', 43, 11, '11', 0, 16, 72, 'Finished', 5924360, '0 days 00:00:14.511000', 4, 72, '0 days 00:01:13.049000');
INSERT INTO public.results VALUES (291, 9, 'lawson', 'rb', 30, 12, '12', 0, 8, 72, 'Finished', 5926912, '0 days 00:00:17.063000', 12, 60, '0 days 00:01:13.879000');
INSERT INTO public.results VALUES (292, 9, 'sainz', 'williams', 55, 13, '13', 0, 9, 72, 'Finished', 5927225, '0 days 00:00:17.376000', 10, 58, '0 days 00:01:13.808000');
INSERT INTO public.results VALUES (293, 9, 'hulkenberg', 'sauber', 27, 14, '14', 0, 17, 72, 'Finished', 5929574, '0 days 00:00:19.725000', 18, 61, '0 days 00:01:14.912000');
INSERT INTO public.results VALUES (294, 9, 'bortoleto', 'sauber', 5, 15, '15', 0, 13, 72, 'Finished', 5931414, '0 days 00:00:21.565000', 15, 63, '0 days 00:01:14.307000');
INSERT INTO public.results VALUES (295, 9, 'antonelli', 'mercedes', 12, 16, '16', 0, 11, 72, 'Finished', 5931878, '0 days 00:00:22.029000', 6, 70, '0 days 00:01:13.480000');
INSERT INTO public.results VALUES (296, 9, 'gasly', 'alpine', 10, 17, '17', 0, 14, 72, 'Finished', 5933478, '0 days 00:00:23.629000', 19, 59, '0 days 00:01:15.248000');
INSERT INTO public.results VALUES (297, 9, 'norris', 'mclaren', 4, 18, '18', 0, 2, 64, 'Retired', 5168487, NULL, 2, 59, '0 days 00:01:12.379000');
INSERT INTO public.results VALUES (298, 9, 'leclerc', 'ferrari', 16, 19, 'R', 0, 6, 52, 'Retired', NULL, NULL, 17, 33, '0 days 00:01:14.557000');
INSERT INTO public.results VALUES (299, 9, 'hamilton', 'ferrari', 44, 20, 'R', 0, 7, 22, 'Retired', NULL, NULL, 20, 6, '0 days 00:01:15.684000');
INSERT INTO public.results VALUES (300, 10, 'max_verstappen', 'red_bull', 1, 1, '1', 25, 1, 53, 'Finished', 4404325, '0 days 01:13:24.325000', 2, 52, '0 days 00:01:21.003000');
INSERT INTO public.results VALUES (301, 10, 'norris', 'mclaren', 4, 2, '2', 18, 2, 53, 'Finished', 4423532, '0 days 00:00:19.207000', 1, 53, '0 days 00:01:20.901000');
INSERT INTO public.results VALUES (302, 10, 'piastri', 'mclaren', 81, 3, '3', 15, 3, 53, 'Finished', 4425676, '0 days 00:00:21.351000', 3, 47, '0 days 00:01:21.245000');
INSERT INTO public.results VALUES (303, 10, 'leclerc', 'ferrari', 16, 4, '4', 12, 4, 53, 'Finished', 4429949, '0 days 00:00:25.624000', 4, 53, '0 days 00:01:21.294000');
INSERT INTO public.results VALUES (304, 10, 'russell', 'mercedes', 63, 5, '5', 10, 5, 53, 'Finished', 4437206, '0 days 00:00:32.881000', 8, 45, '0 days 00:01:21.800000');
INSERT INTO public.results VALUES (305, 10, 'hamilton', 'ferrari', 44, 6, '6', 8, 10, 53, 'Finished', 4441774, '0 days 00:00:37.449000', 6, 50, '0 days 00:01:21.546000');
INSERT INTO public.results VALUES (306, 10, 'albon', 'williams', 23, 7, '7', 6, 14, 53, 'Finished', 4454862, '0 days 00:00:50.537000', 5, 53, '0 days 00:01:21.368000');
INSERT INTO public.results VALUES (307, 10, 'bortoleto', 'sauber', 5, 8, '8', 4, 7, 53, 'Finished', 4462809, '0 days 00:00:58.484000', 12, 51, '0 days 00:01:22.139000');
INSERT INTO public.results VALUES (308, 10, 'antonelli', 'mercedes', 12, 9, '9', 2, 6, 53, 'Finished', 4464087, '0 days 00:00:59.762000', 10, 53, '0 days 00:01:21.968000');
INSERT INTO public.results VALUES (309, 10, 'hadjar', 'rb', 6, 10, '10', 1, 19, 53, 'Finished', 4468216, '0 days 00:01:03.891000', 11, 46, '0 days 00:01:22.133000');
INSERT INTO public.results VALUES (310, 10, 'sainz', 'williams', 55, 11, '11', 0, 13, 53, 'Finished', 4468794, '0 days 00:01:04.469000', 7, 47, '0 days 00:01:21.740000');
INSERT INTO public.results VALUES (311, 10, 'bearman', 'haas', 87, 12, '12', 0, 11, 53, 'Finished', 4483613, '0 days 00:01:19.288000', 9, 53, '0 days 00:01:21.820000');
INSERT INTO public.results VALUES (312, 10, 'tsunoda', 'red_bull', 22, 13, '13', 0, 9, 53, 'Finished', 4485026, '0 days 00:01:20.701000', 16, 52, '0 days 00:01:22.712000');
INSERT INTO public.results VALUES (313, 10, 'lawson', 'rb', 30, 14, '14', 0, 18, 53, 'Finished', 4486676, '0 days 00:01:22.351000', 17, 49, '0 days 00:01:22.777000');
INSERT INTO public.results VALUES (314, 10, 'ocon', 'haas', 31, 15, '15', 0, 15, 52, 'Lapped', 4406460, '0 days 00:00:02.135000', 18, 48, '0 days 00:01:22.892000');
INSERT INTO public.results VALUES (315, 10, 'gasly', 'alpine', 10, 16, '16', 0, 20, 52, 'Lapped', 4410162, '0 days 00:00:05.837000', 14, 52, '0 days 00:01:22.185000');
INSERT INTO public.results VALUES (316, 10, 'colapinto', 'alpine', 43, 17, '17', 0, 17, 52, 'Lapped', 4411773, '0 days 00:00:07.448000', 15, 48, '0 days 00:01:22.239000');
INSERT INTO public.results VALUES (317, 10, 'stroll', 'aston_martin', 18, 18, '18', 0, 16, 52, 'Lapped', 4413626, '0 days 00:00:09.301000', 13, 51, '0 days 00:01:22.164000');
INSERT INTO public.results VALUES (318, 10, 'alonso', 'aston_martin', 14, 19, 'R', 0, 8, 24, 'Retired', NULL, NULL, 19, 23, '0 days 00:01:23.757000');
INSERT INTO public.results VALUES (319, 10, 'hulkenberg', 'sauber', 27, 20, 'W', 0, 12, 0, 'Did not start', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.results VALUES (320, 11, 'max_verstappen', 'red_bull', 1, 1, '1', 25, 1, 51, 'Finished', 5606408, '0 days 01:33:26.408000', 1, 50, '0 days 00:01:43.388000');
INSERT INTO public.results VALUES (321, 11, 'russell', 'mercedes', 63, 2, '2', 18, 5, 51, 'Finished', 5621017, '0 days 00:00:14.609000', 2, 42, '0 days 00:01:43.754000');
INSERT INTO public.results VALUES (322, 11, 'sainz', 'williams', 55, 3, '3', 15, 2, 51, 'Finished', 5625607, '0 days 00:00:19.199000', 4, 47, '0 days 00:01:43.972000');
INSERT INTO public.results VALUES (323, 11, 'antonelli', 'mercedes', 12, 4, '4', 12, 4, 51, 'Finished', 5628168, '0 days 00:00:21.760000', 6, 47, '0 days 00:01:44.091000');
INSERT INTO public.results VALUES (324, 11, 'lawson', 'rb', 30, 5, '5', 10, 3, 51, 'Finished', 5639698, '0 days 00:00:33.290000', 13, 49, '0 days 00:01:44.531000');
INSERT INTO public.results VALUES (325, 11, 'tsunoda', 'red_bull', 22, 6, '6', 8, 6, 51, 'Finished', 5640216, '0 days 00:00:33.808000', 12, 41, '0 days 00:01:44.434000');
INSERT INTO public.results VALUES (326, 11, 'norris', 'mclaren', 4, 7, '7', 6, 7, 51, 'Finished', 5640635, '0 days 00:00:34.227000', 8, 42, '0 days 00:01:44.155000');
INSERT INTO public.results VALUES (327, 11, 'hamilton', 'ferrari', 44, 8, '8', 4, 12, 51, 'Finished', 5642718, '0 days 00:00:36.310000', 5, 40, '0 days 00:01:43.977000');
INSERT INTO public.results VALUES (328, 11, 'leclerc', 'ferrari', 16, 9, '9', 2, 10, 51, 'Finished', 5643182, '0 days 00:00:36.774000', 9, 50, '0 days 00:01:44.274000');
INSERT INTO public.results VALUES (329, 11, 'hadjar', 'rb', 6, 10, '10', 1, 8, 51, 'Finished', 5645390, '0 days 00:00:38.982000', 3, 50, '0 days 00:01:43.884000');
INSERT INTO public.results VALUES (330, 11, 'bortoleto', 'sauber', 5, 11, '11', 0, 13, 51, 'Finished', 5674014, '0 days 00:01:07.606000', 14, 45, '0 days 00:01:44.930000');
INSERT INTO public.results VALUES (331, 11, 'bearman', 'haas', 87, 12, '12', 0, 15, 51, 'Finished', 5674670, '0 days 00:01:08.262000', 10, 31, '0 days 00:01:44.288000');
INSERT INTO public.results VALUES (332, 11, 'albon', 'williams', 23, 13, '13', 0, 19, 51, 'Finished', 5679278, '0 days 00:01:12.870000', 7, 51, '0 days 00:01:44.152000');
INSERT INTO public.results VALUES (333, 11, 'ocon', 'haas', 31, 14, '14', 0, 20, 51, 'Finished', 5683988, '0 days 00:01:17.580000', 17, 50, '0 days 00:01:45.388000');
INSERT INTO public.results VALUES (334, 11, 'alonso', 'aston_martin', 14, 15, '15', 0, 11, 51, 'Finished', 5685115, '0 days 00:01:18.707000', 15, 50, '0 days 00:01:45.002000');
INSERT INTO public.results VALUES (335, 11, 'hulkenberg', 'sauber', 27, 16, '16', 0, 17, 51, 'Finished', 5686645, '0 days 00:01:20.237000', 11, 47, '0 days 00:01:44.370000');
INSERT INTO public.results VALUES (336, 11, 'stroll', 'aston_martin', 18, 17, '17', 0, 14, 51, 'Finished', 5702800, '0 days 00:01:36.392000', 16, 50, '0 days 00:01:45.083000');
INSERT INTO public.results VALUES (337, 11, 'gasly', 'alpine', 10, 18, '18', 0, 18, 50, 'Lapped', 5610273, '0 days 00:00:03.865000', 18, 37, '0 days 00:01:45.492000');
INSERT INTO public.results VALUES (338, 11, 'colapinto', 'alpine', 43, 19, '19', 0, 16, 50, 'Lapped', 5612733, '0 days 00:00:06.325000', 19, 40, '0 days 00:01:46.055000');
INSERT INTO public.results VALUES (339, 11, 'piastri', 'mclaren', 81, 20, 'R', 0, 9, 0, 'Retired', NULL, NULL, NULL, NULL, NULL);


--
-- Data for Name: sprint_results; Type: TABLE DATA; Schema: public; Owner: f1_user
--

INSERT INTO public.sprint_results VALUES (111, 8, 'max_verstappen', 'red_bull', 1, 1, '1', 8, 2, 'Finished', 15, '0 days 00:01:46.052000', 2, 6, '0 days 00:26:37.997000', 1597997);
INSERT INTO public.sprint_results VALUES (112, 8, 'piastri', 'mclaren', 81, 2, '2', 7, 1, 'Finished', 15, '0 days 00:01:46.061000', 3, 6, '0 days 00:00:00.753000', 1598750);
INSERT INTO public.sprint_results VALUES (113, 8, 'norris', 'mclaren', 4, 3, '3', 6, 3, 'Finished', 15, '0 days 00:01:45.914000', 1, 6, '0 days 00:00:01.414000', 1599411);
INSERT INTO public.sprint_results VALUES (114, 8, 'leclerc', 'ferrari', 16, 4, '4', 5, 4, 'Finished', 15, '0 days 00:01:46.343000', 4, 2, '0 days 00:00:10.176000', 1608173);
INSERT INTO public.sprint_results VALUES (115, 8, 'ocon', 'haas', 31, 5, '5', 4, 5, 'Finished', 15, '0 days 00:01:46.772000', 7, 2, '0 days 00:00:13.789000', 1611786);
INSERT INTO public.sprint_results VALUES (116, 8, 'sainz', 'williams', 55, 6, '6', 3, 6, 'Finished', 15, '0 days 00:01:46.770000', 6, 7, '0 days 00:00:14.964000', 1612961);
INSERT INTO public.sprint_results VALUES (117, 8, 'bearman', 'haas', 87, 7, '7', 2, 7, 'Finished', 15, '0 days 00:01:47.038000', 9, 2, '0 days 00:00:18.610000', 1616607);
INSERT INTO public.sprint_results VALUES (118, 8, 'hadjar', 'rb', 6, 8, '8', 1, 9, 'Finished', 15, '0 days 00:01:46.973000', 8, 2, '0 days 00:00:19.119000', 1617116);
INSERT INTO public.sprint_results VALUES (119, 8, 'bortoleto', 'sauber', 5, 9, '9', 0, 10, 'Finished', 15, '0 days 00:01:47.086000', 10, 2, '0 days 00:00:22.183000', 1620180);
INSERT INTO public.sprint_results VALUES (120, 8, 'lawson', 'rb', 30, 10, '10', 0, 11, 'Finished', 15, '0 days 00:01:47.249000', 12, 2, '0 days 00:00:22.897000', 1620894);
INSERT INTO public.sprint_results VALUES (121, 8, 'tsunoda', 'red_bull', 22, 11, '11', 0, 12, 'Finished', 15, '0 days 00:01:47.326000', 15, 4, '0 days 00:00:24.551000', 1622548);
INSERT INTO public.sprint_results VALUES (122, 8, 'russell', 'mercedes', 63, 12, '12', 0, 13, 'Finished', 15, '0 days 00:01:47.278000', 13, 4, '0 days 00:00:25.969000', 1623966);
INSERT INTO public.sprint_results VALUES (123, 8, 'stroll', 'aston_martin', 18, 13, '13', 0, 15, 'Finished', 15, '0 days 00:01:47.307000', 14, 5, '0 days 00:00:26.595000', 1624592);
INSERT INTO public.sprint_results VALUES (124, 8, 'alonso', 'aston_martin', 14, 14, '14', 0, 14, 'Finished', 15, '0 days 00:01:47.444000', 17, 5, '0 days 00:00:29.046000', 1627043);
INSERT INTO public.sprint_results VALUES (125, 8, 'hamilton', 'ferrari', 44, 15, '15', 0, 18, 'Finished', 15, '0 days 00:01:47.201000', 11, 4, '0 days 00:00:30.175000', 1628172);
INSERT INTO public.sprint_results VALUES (126, 8, 'albon', 'williams', 23, 16, '16', 0, 16, 'Finished', 15, '0 days 00:01:47.419000', 16, 6, '0 days 00:00:30.941000', 1628938);
INSERT INTO public.sprint_results VALUES (127, 8, 'antonelli', 'mercedes', 12, 17, '17', 0, 19, 'Finished', 15, '0 days 00:01:46.698000', 5, 5, '0 days 00:00:31.981000', 1629978);
INSERT INTO public.sprint_results VALUES (128, 8, 'hulkenberg', 'sauber', 27, 18, '18', 0, 17, 'Finished', 15, '0 days 00:01:47.575000', 18, 8, '0 days 00:00:32.867000', 1630864);
INSERT INTO public.sprint_results VALUES (129, 8, 'colapinto', 'alpine', 43, 19, '19', 0, 20, 'Finished', 15, '0 days 00:01:47.944000', 20, 15, '0 days 00:00:38.072000', 1636069);
INSERT INTO public.sprint_results VALUES (130, 8, 'gasly', 'alpine', 10, 20, 'R', 0, 8, 'Retired', 12, '0 days 00:01:47.651000', 19, 6, NULL, NULL);
INSERT INTO public.sprint_results VALUES (71, 1, 'hamilton', 'ferrari', 44, 1, '1', 8, 1, 'Finished', 19, '0 days 00:01:35.399000', 1, 2, '0 days 00:30:39.965000', 1839965);
INSERT INTO public.sprint_results VALUES (72, 1, 'piastri', 'mclaren', 81, 2, '2', 7, 3, 'Finished', 19, '0 days 00:01:35.854000', 4, 7, '0 days 00:00:06.889000', 1846854);
INSERT INTO public.sprint_results VALUES (73, 1, 'max_verstappen', 'red_bull', 1, 3, '3', 6, 2, 'Finished', 19, '0 days 00:01:35.745000', 2, 2, '0 days 00:00:09.804000', 1849769);
INSERT INTO public.sprint_results VALUES (74, 1, 'russell', 'mercedes', 63, 4, '4', 5, 5, 'Finished', 19, '0 days 00:01:35.891000', 5, 4, '0 days 00:00:11.592000', 1851557);
INSERT INTO public.sprint_results VALUES (75, 1, 'leclerc', 'ferrari', 16, 5, '5', 4, 4, 'Finished', 19, '0 days 00:01:36.255000', 6, 4, '0 days 00:00:12.190000', 1852155);
INSERT INTO public.sprint_results VALUES (76, 1, 'tsunoda', 'rb', 22, 6, '6', 3, 8, 'Finished', 19, '0 days 00:01:36.388000', 8, 4, '0 days 00:00:22.288000', 1862253);
INSERT INTO public.sprint_results VALUES (77, 1, 'antonelli', 'mercedes', 12, 7, '7', 2, 7, 'Finished', 19, '0 days 00:01:36.311000', 7, 5, '0 days 00:00:23.038000', 1863003);
INSERT INTO public.sprint_results VALUES (78, 1, 'norris', 'mclaren', 4, 8, '8', 1, 6, 'Finished', 19, '0 days 00:01:36.708000', 11, 4, '0 days 00:00:23.471000', 1863436);
INSERT INTO public.sprint_results VALUES (79, 1, 'stroll', 'aston_martin', 18, 9, '9', 0, 10, 'Finished', 19, '0 days 00:01:36.435000', 9, 4, '0 days 00:00:24.916000', 1864881);
INSERT INTO public.sprint_results VALUES (80, 1, 'alonso', 'aston_martin', 14, 10, '10', 0, 11, 'Finished', 19, '0 days 00:01:37.058000', 12, 8, '0 days 00:00:38.218000', 1878183);
INSERT INTO public.sprint_results VALUES (81, 1, 'albon', 'williams', 23, 11, '11', 0, 9, 'Finished', 19, '0 days 00:01:37.344000', 15, 7, '0 days 00:00:39.292000', 1879257);
INSERT INTO public.sprint_results VALUES (82, 1, 'gasly', 'alpine', 10, 12, '12', 0, 17, 'Finished', 19, '0 days 00:01:37.481000', 17, 3, '0 days 00:00:39.649000', 1879614);
INSERT INTO public.sprint_results VALUES (83, 1, 'hadjar', 'rb', 6, 13, '13', 0, 15, 'Finished', 19, '0 days 00:01:37.549000', 18, 3, '0 days 00:00:42.400000', 1882365);
INSERT INTO public.sprint_results VALUES (84, 1, 'lawson', 'red_bull', 30, 14, '14', 0, 19, 'Finished', 19, '0 days 00:01:37.163000', 14, 4, '0 days 00:00:44.904000', 1884869);
INSERT INTO public.sprint_results VALUES (85, 1, 'bearman', 'haas', 87, 15, '15', 0, 12, 'Finished', 19, '0 days 00:01:37.135000', 13, 3, '0 days 00:00:45.649000', 1885614);
INSERT INTO public.sprint_results VALUES (86, 1, 'ocon', 'haas', 31, 16, '16', 0, 18, 'Finished', 19, '0 days 00:01:37.554000', 19, 3, '0 days 00:00:46.182000', 1886147);
INSERT INTO public.sprint_results VALUES (87, 1, 'sainz', 'williams', 55, 17, '17', 0, 13, 'Finished', 19, '0 days 00:01:35.819000', 3, 13, '0 days 00:00:51.376000', 1891341);
INSERT INTO public.sprint_results VALUES (88, 1, 'bortoleto', 'sauber', 5, 18, '18', 0, 14, 'Finished', 19, '0 days 00:01:37.475000', 16, 3, '0 days 00:00:53.940000', 1893905);
INSERT INTO public.sprint_results VALUES (89, 1, 'hulkenberg', 'sauber', 27, 19, '19', 0, 20, 'Finished', 19, '0 days 00:01:36.529000', 10, 4, '0 days 00:00:56.682000', 1896647);
INSERT INTO public.sprint_results VALUES (90, 1, 'doohan', 'alpine', 7, 20, '20', 0, 16, 'Finished', 19, '0 days 00:01:37.686000', 20, 3, '0 days 00:01:10.212000', 1910177);
INSERT INTO public.sprint_results VALUES (91, 4, 'norris', 'mclaren', 4, 1, '1', 8, 3, 'Finished', 18, '0 days 00:01:40.334000', 5, 4, '0 days 00:36:37.647000', 2197647);
INSERT INTO public.sprint_results VALUES (92, 4, 'piastri', 'mclaren', 81, 2, '2', 7, 2, 'Finished', 18, '0 days 00:01:40.238000', 4, 7, '0 days 00:00:00.672000', 2198319);
INSERT INTO public.sprint_results VALUES (93, 4, 'hamilton', 'ferrari', 44, 3, '3', 6, 7, 'Finished', 18, '0 days 00:01:36.368000', 1, 13, '0 days 00:00:01.073000', 2198720);
INSERT INTO public.sprint_results VALUES (94, 4, 'russell', 'mercedes', 63, 4, '4', 5, 5, 'Finished', 18, '0 days 00:01:40.963000', 7, 6, '0 days 00:00:03.127000', 2200774);
INSERT INTO public.sprint_results VALUES (95, 4, 'stroll', 'aston_martin', 18, 5, '5', 4, 16, 'Finished', 18, '0 days 00:01:36.839000', 2, 13, '0 days 00:00:03.412000', 2201059);
INSERT INTO public.sprint_results VALUES (96, 4, 'tsunoda', 'red_bull', 22, 6, '6', 3, 20, 'Finished', 18, '0 days 00:01:38.078000', 3, 13, '0 days 00:00:05.153000', 2202800);
INSERT INTO public.sprint_results VALUES (97, 4, 'antonelli', 'mercedes', 12, 7, '7', 2, 1, 'Finished', 18, '0 days 00:01:41.012000', 8, 6, '0 days 00:00:05.635000', 2203282);
INSERT INTO public.sprint_results VALUES (98, 4, 'gasly', 'alpine', 10, 8, '8', 1, 13, 'Finished', 18, '0 days 00:01:42.694000', 16, 7, '0 days 00:00:05.973000', 2203620);
INSERT INTO public.sprint_results VALUES (99, 4, 'hulkenberg', 'sauber', 27, 9, '9', 0, 11, 'Finished', 18, '0 days 00:01:42.871000', 17, 5, '0 days 00:00:06.153000', 2203800);
INSERT INTO public.sprint_results VALUES (100, 4, 'hadjar', 'rb', 6, 10, '10', 0, 9, 'Finished', 18, '0 days 00:01:42.260000', 13, 6, '0 days 00:00:07.502000', 2205149);
INSERT INTO public.sprint_results VALUES (101, 4, 'albon', 'williams', 23, 11, '11', 0, 8, 'Finished', 18, '0 days 00:01:41.699000', 9, 7, '0 days 00:00:07.522000', 2205169);
INSERT INTO public.sprint_results VALUES (102, 4, 'ocon', 'haas', 31, 12, '12', 0, 12, 'Finished', 18, '0 days 00:01:42.550000', 14, 6, '0 days 00:00:08.998000', 2206645);
INSERT INTO public.sprint_results VALUES (103, 4, 'lawson', 'rb', 30, 13, '13', 0, 14, 'Finished', 18, '0 days 00:01:41.922000', 11, 7, '0 days 00:00:09.024000', 2206671);
INSERT INTO public.sprint_results VALUES (104, 4, 'bearman', 'haas', 87, 14, '14', 0, 19, 'Finished', 18, '0 days 00:01:42.237000', 12, 5, '0 days 00:00:09.218000', 2206865);
INSERT INTO public.sprint_results VALUES (105, 4, 'bortoleto', 'sauber', 5, 15, '15', 0, 18, 'Finished', 18, '0 days 00:01:42.989000', 18, 6, '0 days 00:00:09.675000', 2207322);
INSERT INTO public.sprint_results VALUES (106, 4, 'doohan', 'alpine', 7, 16, '16', 0, 17, 'Finished', 18, '0 days 00:01:43.076000', 19, 7, '0 days 00:00:09.909000', 2207556);
INSERT INTO public.sprint_results VALUES (107, 4, 'max_verstappen', 'red_bull', 1, 17, '17', 0, 4, 'Finished', 18, '0 days 00:01:40.697000', 6, 5, '0 days 00:00:12.059000', 2209706);
INSERT INTO public.sprint_results VALUES (108, 4, 'alonso', 'aston_martin', 14, 18, 'R', 0, 10, 'Retired', 13, '0 days 00:01:41.782000', 10, 7, '', NULL);
INSERT INTO public.sprint_results VALUES (109, 4, 'sainz', 'williams', 55, 19, 'R', 0, 15, 'Retired', 12, '0 days 00:01:42.638000', 15, 5, '', NULL);
INSERT INTO public.sprint_results VALUES (110, 4, 'leclerc', 'ferrari', 16, 20, 'R', 0, 6, 'Retired', 0, '', NULL, NULL, '', NULL);


--
-- Name: constructor_standings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.constructor_standings_id_seq', 130, true);


--
-- Name: driver_seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.driver_seasons_id_seq', 42, true);


--
-- Name: driver_standings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.driver_standings_id_seq', 255, true);


--
-- Name: qualifying_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.qualifying_results_id_seq', 540, true);


--
-- Name: races_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.races_id_seq', 25, true);


--
-- Name: results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.results_id_seq', 339, true);


--
-- Name: seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.seasons_id_seq', 3, true);


--
-- Name: sprint_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: f1_user
--

SELECT pg_catalog.setval('public.sprint_results_id_seq', 130, true);


--
-- PostgreSQL database dump complete
--

