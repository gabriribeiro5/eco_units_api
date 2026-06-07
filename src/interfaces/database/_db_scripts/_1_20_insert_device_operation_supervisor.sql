-- Insert BACKUSER with device_operation_agent_id
INSERT IGNORE INTO `device_operation_supervisor`
(`device_operation_supervisor_id`,
`agent_id`,
`device_operation_supervisor_email`,
`device_operation_supervisor_name`,
`device_operation_supervisor_surname`,
`device_operation_supervisor_secret`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s,
%s);