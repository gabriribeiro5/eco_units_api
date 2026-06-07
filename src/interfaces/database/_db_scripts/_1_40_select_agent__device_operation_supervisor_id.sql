-- select device_operation_supervisor_id for a given device_operation_agent_id
SELECT device_operation_supervisor_id
FROM device_operation_agent
WHERE device_operation_agent_id = %s;