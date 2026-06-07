-- Insert device operation agent but do NOT enable
INSERT IGNORE INTO `agent`
( `agent_id`,
`backoffice_admin_id`,
`device_operation_agent_id`,
`supply_chain_manager_id`,
`sales_service_id`,
`creation_date_time`,
`is_enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled