-- Insert BACKUSER_ADMIN with agent_id
INSERT IGNORE INTO backuser_admin
(`backuser_admin_id`,
`agent_id`,
`backuser_admin_email`,
`backuser_admin_name`,
`backuser_admin_surname`,
`backuser_admin_secret`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s,
%s);