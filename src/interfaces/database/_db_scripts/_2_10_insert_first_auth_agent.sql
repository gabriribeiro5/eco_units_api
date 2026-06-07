-- insert first auth token
INSERT IGNORE INTO `first_auth_device_operation_agent`
(`device_operation_agent_id`,
`token`)
VALUES
(%s,
%s);