-- Select first-auth token for an agent
SELECT
    `token`
FROM
    `first_auth_agent`
WHERE
    `agent_id` = %s;