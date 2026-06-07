-- ------------------------------------
-- -> device insert: self diagnostic
-- ------------------------------------

INSERT IGNORE INTO `diagnostic`
(`diagnostic_id`,
`device_id`,
`device_operation_agent_id`,
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
		from device_operation_agent as ainput 
        order by ainput.date_time
        limit 1),
	(select ainput.device_operation_agent_id
		from device_operation_agent as ainput 
        order by ainput.date_time
        limit 1),
'2024-10-30 07:55:00.000000',
'cyclobot says: so far so good',
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1, -- 1 = running; 2 = malfunction; 3 = not installed
1); -- 1 = running; 2 = malfunction; 3 = not installed
