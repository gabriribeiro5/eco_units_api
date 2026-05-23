-- Enable DEVICE
UPDATE `agent`
SET
device_id = %s
WHERE `agent_id` = %s;
