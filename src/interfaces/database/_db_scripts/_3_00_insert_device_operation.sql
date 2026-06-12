-- Insert a default device_operation_agent row for device operation tracking
INSERT IGNORE INTO `device_operation_agent`
(`device_operation_agent_id`,
`agent_id`,
`supervisor_id`,
`device_id`,
`customer_id`,
`creation_date_time`)
VALUES
(DEFAULT,
%s,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP);