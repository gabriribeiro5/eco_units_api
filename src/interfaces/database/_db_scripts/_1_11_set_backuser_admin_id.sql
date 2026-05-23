-- Enable BACKUSER_ADMIN
UPDATE `agent`
SET
backuser_admin_id = %s
WHERE `agent_id` = %s;
