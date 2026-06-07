-- ---------------------------------------
-- -> device insert: ecosystem state
-- ---------------------------------------

INSERT IGNORE INTO `ecosystem_state`
(`ecosystem_state_id`,
`device_id`,
`device_operation_agent_id`,
`scan_date_time`,
`soil_moisture`,
`temperature`,
`rain_occurrences_per_day`)
VALUES
(DEFAULT,
	(select ainput.device_id
		from device_operation_agent as ainput
        order by ainput.date_time desc
        limit 1),
	(select ainput.device_operation_agent_id
		from device_operation_agent as ainput
        order by ainput.date_time desc
        limit 1),
'2024-10-30 09:00:00.000000',
200,
18,
0);