-- Select device_operation_agent enabled state
SELECT
    `is_enabled`
FROM
    `device_operation_agent`
WHERE
    device_operation_agent_id = %s;