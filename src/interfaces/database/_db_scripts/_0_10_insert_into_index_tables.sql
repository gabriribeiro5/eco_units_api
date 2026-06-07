/* POPULATE DATABASE FOR TESTS AND DEVELOPMENT */

-- ------------------------
-- POPULATING INDEX TABLES
-- ------------------------

-- -----------------------------------------
-- Sensor status (ignore insert if PK or FK already exists)
-- -----------------------------------------
INSERT IGNORE INTO `component_status`
(`component_status_id`,
`component_status_name`,
`component_status_description`)
VALUES
(1,
'RUNNING',
'Physical component is up and running'),
(2,
'MALFUNCTION',
'Ops... Physical component not working'),
(3,
'NOT INSTALLED',
'The referenced cyclobot does not have this physical component')
AS `new`
ON DUPLICATE KEY UPDATE component_status_name = `new`.component_status_name,
 component_status_description = `new`.component_status_description;

-- -----------------------------------------
-- Config status (ignore insert if PK or FK already exists)
-- -----------------------------------------
INSERT IGNORE INTO `config_status`
(`config_status_id`,
`status_name`,
`status_description`)
VALUES
(1,
"CONFIRMED",
"configuration data declared by cyclobot only"),
(2,
"SENT",
"configuration update data sent to cyclobot"),
(3,
"WAITING",
"configuration update data wating to be sent"),
(4,
"EXPIRED",
"configuration update data that has not been (and will not be) sent to cyclobot")
AS `new`
ON DUPLICATE KEY UPDATE status_name = `new`.status_name,
 status_description = `new`.status_description;

-- -----------------------------------------
-- Climate season (ignore insert if PK or FK already exists)
-- -----------------------------------------
INSERT IGNORE INTO `climate_season`
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
AS `new`
ON DUPLICATE KEY UPDATE season_name = `new`.season_name;

INSERT IGNORE INTO `device_strategy`
(`device_strategy_id`,
`strategy_full_name`,
`strategy_description`,
`min_temperature_expected`,
`max_temperature_expected`)
VALUES
(1,
'VEGETABLE GARDEN',
'Eco_unit is expected to work as a propper growth box',
NULL,
NULL
),
(2,
'PET HABITAT',
'Here systems must serve the animal life',
NULL,
NULL
),
(3,
'RAINFOREST',
'Where the rain is key to life',
NULL,
NULL
),
(4,
'SWAMP',
'Why would you want it',
NULL,
NULL
),
(5,
'PRAIRIE',
'Haja mato',
NULL,
NULL)
AS `new`
ON DUPLICATE KEY UPDATE strategy_full_name = `new`.strategy_full_name,
 strategy_description = `new`.strategy_description;