-- insert session token
INSERT IGNORE INTO `session`
(`agent_id`,
`token`)
VALUES
(%s,
%s);