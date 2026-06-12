-- Insert a generic agent row but do NOT enable it
INSERT IGNORE INTO `agent`
(`agent_id`,
`backoffice_admin_id`,
`device_operation_agent_id`,
`supply_chain_manager_id`,
`creation_date_time`,
`is_enabled`)
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0);