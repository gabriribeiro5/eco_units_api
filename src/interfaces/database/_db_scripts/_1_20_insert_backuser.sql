-- Insert BACKUSER with agent_id
INSERT IGNORE INTO backuser
(`backuser_id`,
`agent_id`,
`backuser_email`,
`backuser_name`,
`backuser_surname`,
`backuser_secret`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s,
%s);