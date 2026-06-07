-- delete first auth token for a device_operation_agent
DELETE IGNORE FROM `first_auth_device_operation_agent`
WHERE `device_operation_agent_id` = %s;