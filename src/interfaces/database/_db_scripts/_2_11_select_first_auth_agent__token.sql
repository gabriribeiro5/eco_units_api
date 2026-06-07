-- Select first auth device operation agent token
SELECT
    `token`
FROM
    `first_auth_device_operation_agent`
WHERE
    device_operation_agent_id = %s;