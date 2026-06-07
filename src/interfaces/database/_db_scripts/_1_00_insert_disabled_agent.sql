-- Insert device operation agent but do NOT enable
INSERT IGNORE INTO `device_operation_agent`
(`device_operation_agent_id`,
  `device_operation_supervisor_id`,
  `customer_id`,
  `device_id`,
  `creation_date_time`,
  `is_enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled