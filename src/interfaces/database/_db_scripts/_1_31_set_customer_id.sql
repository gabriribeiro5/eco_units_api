-- Associate CUSTOMER with the device_operation_agent row
UPDATE `device_operation_agent`
SET
customer_id = %s
WHERE `device_operation_agent_id` = %s;
