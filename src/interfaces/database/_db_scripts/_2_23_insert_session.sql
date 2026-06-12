-- Insert a session token for an agent
INSERT IGNORE INTO `session`
(`agent_id`,
`token`,
`max_lenght_session`)
VALUES
(%s,
%s,
NULL);