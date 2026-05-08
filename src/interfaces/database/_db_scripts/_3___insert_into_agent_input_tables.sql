/* POPULATE DATABASE FOR TESTS AND DEVELOPMENT */

-- -----------------------------------------------
--               AGENT INPUTS
-- -----------------------------------------------
--                 Summary
--                  to do
-- -> device insert: self diagnostic
-- -> device insert: current configuration
-- -> device insert: environment state
-- 
-- -> back user insert: unit diagnostic
-- -> back user insert: unit configuration update
-- 
-- -> customer insert: unit diagnostic
-- -> customer insert: unit configuration update
-- -----------------------------------------------

-- ------------------------------------
-- -> device insert: self diagnostic
-- ------------------------------------

-- device input
INSERT IGNORE INTO agent_input
(`agent_input_id`,
`agent_id`,
`device_id`,
`date_time`,
`failed_communication`)
VALUES
(DEFAULT,
	(select d.agent_id
		from device as d
        order by d.device_id desc
        limit 1),
	(select d.device_id
		from device as d
        order by d.device_id desc
        limit 1),
CURRENT_TIMESTAMP,
0);

INSERT IGNORE INTO `ecosystem_db`.`diagnostic`
(`diagnostic_id`,
`device_id`,
`agent_input_id`,
`diagnostic_date_time`,
`device_message`,
`wifi_connected`,
`watering_system`,
`river_system`,
`wind_system`,
`lighting_system`)
VALUES
(DEFAULT,
	(select ainput.device_id 
		from agent_input as ainput 
        order by ainput.date_time
        limit 1),
	(select ainput.agent_input_id
		from agent_input as ainput 
        order by ainput.date_time
        limit 1),
'2024-10-30 07:55:00.000000',
'cyclobot says: so far so good',
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1); -- 1 = running; 2 = malfunction; 3 = not installed

-- ------------------------------------------
-- -> device insert: current configuration
-- ------------------------------------------

-- device input
INSERT IGNORE INTO agent_input
(`agent_input_id`,
`agent_id`,
`device_id`,
`date_time`,
`failed_communication`)
VALUES
(DEFAULT,
	(select d.agent_id
		from device as d
        order by d.device_id desc
        limit 1),
	(select d.device_id
		from device as d
        order by d.device_id desc
        limit 1),
CURRENT_TIMESTAMP,
0);

INSERT IGNORE INTO `configuration`
(`configuration_id`,
`device_id`,
`agent_input_id`,
`config_status_id`, -- 1 = confirmed; 2 = sent; 3 = wating; 4 = expired
`run_physical_diagnostics`,
`soil_moisture_max`,
`soil_moisture_min`,
`watering_initial_lenght`,
`watering_lenght_growth_rate`,
`watering_lenght_decrease_rate`,
`expected_climate_season`)
VALUES
(DEFAULT,
	(select ainput.device_id
		from agent_input as ainput
        order by ainput.date_time desc
        limit 1),
	(select ainput.agent_input_id
		from agent_input as ainput
        order by ainput.date_time desc
        limit 1),
1, -- 1 = confirmed; 2 = sent; 3 = wating; 4 = expired
1,
400, -- soil_moisture_max
250, -- soil_moisture_min
3, -- watering_initial_lenght
2, -- watering_lenght_growth_rate
2, -- watering_lenght_decrease_rate
4); -- 1=Summer, 2=Autumn, 3=Winter, 4=Spring


-- ---------------------------------------
-- -> device insert: environment state
-- ---------------------------------------

-- device input
INSERT IGNORE INTO agent_input
(`agent_input_id`,
`agent_id`,
`device_id`,
`date_time`,
`failed_communication`)
VALUES
(DEFAULT,
	(select d.agent_id
		from device as d
        order by d.device_id desc
        limit 1),
	(select d.device_id
		from device as d
        order by d.device_id desc
        limit 1),
CURRENT_TIMESTAMP,
0);

INSERT IGNORE INTO ecosystem_state
(`ecosystem_state_id`,
`device_id`,
`agent_input_id`,
`scan_date_time`,
`soil_moisture`,
`temperature`,
`rain_occurrences_per_day`)
VALUES
(DEFAULT,
	(select ainput.device_id
		from agent_input as ainput
        order by ainput.date_time desc
        limit 1),
	(select ainput.agent_input_id
		from agent_input as ainput
        order by ainput.date_time desc
        limit 1),
'2024-10-30 09:00:00.000000',
200,
18,
0);