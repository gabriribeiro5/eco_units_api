-- Insert CUSTOMER with agent_id
INSERT IGNORE INTO customer
(`customer_id`,
`agent_id`,
`customer_name`,
`customer_surname`,
`customer_email`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s);