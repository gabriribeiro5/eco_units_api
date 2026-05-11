-- Enable BACKUSER
UPDATE `agent`
SET
backuser_id = %s
WHERE `agent_id` = %s;
