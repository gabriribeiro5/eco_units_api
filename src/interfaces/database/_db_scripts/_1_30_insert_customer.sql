-- Insert CUSTOMER with device_operation_agent_id
INSERT IGNORE INTO customer
(`customer_id`,
`device_operation_agent_id`,
`customer_email`,
`customer_name`,
`customer_surname`,
`customer_secret`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s,
%s);