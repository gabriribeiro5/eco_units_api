-- ------------------------------------
-- -> device insert: self diagnostic
-- ------------------------------------

INSERT IGNORE INTO `diagnostic`
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
