-- Select the enabled state of an agent
SELECT
    `is_enabled`
FROM
    `agent`
WHERE
    `agent_id` = %s;