-- select session token
SELECT `token`
FROM `session`
WHERE `device_operation_agent_id` = %s