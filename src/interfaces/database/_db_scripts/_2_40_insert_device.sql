-- Insert DEVICE with agent_id
INSERT IGNORE INTO `device`
(`device_id`,
`agent_id`,
`device_name`,
`customer_id`,
`ecossys_category_id`,
`require_update`,
`location`,
`deactivated`)
VALUES
(DEFAULT,
%s,
%s,
%s, -- ATENTION
%s, -- 1 = VEGETABLE GARDEN, 2 = PET HABITAT, 3 = RAINFOREST...
%s,
%s,
%s);