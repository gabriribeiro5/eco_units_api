-- Associate DEVICE with the device_operation_agent row
UPDATE `device_operation_agent`
SET
device_id = %s
WHERE `device_operation_agent_id` = %s;
