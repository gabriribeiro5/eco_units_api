-- Select the supervisor id associated with a given agent
SELECT doa.`supervisor_id`
FROM `device_operation_agent` AS doa
JOIN `agent` AS a ON a.`device_operation_agent_id` = doa.`device_operation_agent_id`
WHERE a.`agent_id` = %s;