/* POPULATE DATABASE FOR TESTS AND DEVELOPMENT */

-- ------------------------
-- POPULATING INDEX TABLES
-- ------------------------

-- -----------------------------------------
-- Sensor status
-- -----------------------------------------
select * from sensor_status;
INSERT INTO `sensor_status`
(`sensor_status_id`,
`sensor_status_name`,
`sensor_status_description`)
VALUES
(1,
'RUNNING',
'Physical component is up and running'),
(2,
'MALFUNCTION',
'Ops... Physical component not working'),
(3,
'NOT INSTALLED',
'The referenced eco_unit does not have this physical component')
ON DUPLICATE KEY UPDATE sensor_status_name = sensor_status_name,
 sensor_status_description = sensor_status_description;

select * from config_status;
INSERT INTO `config_status`
(`config_status_id`,
`status_name`,
`status_description`)
VALUES
(1,
"CONFIRMED",
"configuration data declared by eco_unit only"),
(2,
"SENT",
"configuration update data sent to eco_unit"),
(3,
"WAITING",
"configuration update data wating to be sent"),
(4,
"EXPIRED",
"configuration update data that has not been (and will not be) sent to eco_unit")
ON DUPLICATE KEY UPDATE status_name = status_name,
 status_description = status_description;

select * from climate_season;
INSERT INTO `climate_season`
(`climate_season_id`,
`season_name`)
VALUES
(1,
"SUMMER"),
(2,
"AUTUMN"),
(3,
"WINTER"),
(4,
"SRPING")
ON DUPLICATE KEY UPDATE season_name = VALUES(season_name);

select * from ecosystem_category;
INSERT INTO ecosystem_category
(`ecosystem_category_id`,
`category_name`,
`category_description`)
VALUES
(1,
'VEGETABLE GARDEN',
'Eco_unit is expected to work as a propper growth box'
),
(2,
'PET HABITAT',
'Here systems must serve the animal life'),
(3,
'RAINFOREST',
'Where the rain is key to life'),
(4,
'SWAMP',
'Why would you want it'),
(5,
'PRAIRIE',
'Haja mato')
ON DUPLICATE KEY UPDATE category_name = category_name,
 category_description = category_description;