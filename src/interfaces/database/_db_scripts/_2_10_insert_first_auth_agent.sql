-- insert first auth token
INSERT IGNORE INTO `first_auth_agent`
(`agent_id`,
`token`)
VALUES
(%s,
%s);