-- select device_secret for a given device_operation_agent_id
SELECT device_secret
FROM `device`
WHERE `device_operation_agent_id` = %s;