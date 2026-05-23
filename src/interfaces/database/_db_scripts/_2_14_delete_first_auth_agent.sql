-- insert first auth token
DELETE IGNORE FROM `first_auth_agent`
WHERE `agent_id` = %s;