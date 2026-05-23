-- delete session for a given token
DELETE FROM `sessions`
WHERE `agent_id` = %s;