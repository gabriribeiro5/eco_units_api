-- Enable an agent
UPDATE `agent`
SET
`is_enabled` = 1
WHERE `agent_id` = %s;
