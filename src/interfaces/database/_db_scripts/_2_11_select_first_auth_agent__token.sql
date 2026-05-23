-- Select first auth agent token
SELECT
    `token`
FROM
    `first_auth_agent`
WHERE
    agent_id = %s;