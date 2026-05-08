-- ------------------------------------------
-- -> device insert: current configuration
-- ------------------------------------------

INSERT IGNORE INTO `device_configuration`
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
