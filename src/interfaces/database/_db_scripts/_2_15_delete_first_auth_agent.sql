-- Delete the first-auth token for an agent
DELETE IGNORE FROM `first_auth_agent`
WHERE `agent_id` = %s;