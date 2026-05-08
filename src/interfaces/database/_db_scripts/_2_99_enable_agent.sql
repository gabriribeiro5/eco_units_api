-- Enable BACK_USER
UPDATE `agent`
SET
enabled = 1
WHERE `agent_id` = %s;
