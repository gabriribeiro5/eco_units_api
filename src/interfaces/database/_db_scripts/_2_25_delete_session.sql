-- Delete all sessions for a given agent
DELETE FROM `session`
WHERE `agent_id` = %s;