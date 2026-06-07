-- Insert BACKUSER_ADMIN with device_operation_agent_id
INSERT IGNORE INTO `backoffice_admin`
(`backoffice_admin_id`,
`agent_id`,
`backoffice_admin_email`,
`backoffice_admin_name`,
`backoffice_admin_surname`,
`backoffice_admin_secret`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s,
%s);