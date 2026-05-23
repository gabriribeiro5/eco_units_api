-- Insert agent but do NOT enable
INSERT IGNORE INTO `agent`
(`agent_id`,
  `device_id`,
  `backuser_id`,
  `customer_id`,
  `creation_date_time`,
  `is_enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled