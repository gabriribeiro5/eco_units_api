-- insert session token
INSERT IGNORE INTO `session`
(`device_operation_agent_id`,
`token`)
VALUES
(%s,
%s);