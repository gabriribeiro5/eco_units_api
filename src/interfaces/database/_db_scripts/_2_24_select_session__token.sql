-- select session token
SELECT `token`
FROM `session`
WHERE `agent_id` = %s