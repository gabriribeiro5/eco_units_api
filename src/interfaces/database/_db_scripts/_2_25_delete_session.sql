-- delete session for a given device_operation_agent
DELETE FROM `session`
WHERE `device_operation_agent_id` = %s;