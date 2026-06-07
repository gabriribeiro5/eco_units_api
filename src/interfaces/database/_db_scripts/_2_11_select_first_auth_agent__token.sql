-- Select first auth device operation agent token
SELECT
    `token`
FROM
    `first_auth_agent`
WHERE
    device_operation_agent_id = %s;