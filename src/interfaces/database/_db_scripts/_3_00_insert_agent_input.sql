-- agent input
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