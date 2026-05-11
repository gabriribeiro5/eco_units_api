-- Enable CUSTOMER
UPDATE `agent`
SET
customer_id = %s
WHERE `agent_id` = %s;
