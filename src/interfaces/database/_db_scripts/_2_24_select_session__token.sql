-- select session token
SELECT `token`
FROM `sessions`
WHERE `agent_id` = %s