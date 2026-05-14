-- Insert BACKUSER with agent_id
INSERT IGNORE INTO backuser
(`backuser_id`,
`agent_id`,
`backuser_name`,
`backuser_surname`,
`backuser_email`)
VALUES
(DEFAULT,
%s,
%s,
%s,
%s);