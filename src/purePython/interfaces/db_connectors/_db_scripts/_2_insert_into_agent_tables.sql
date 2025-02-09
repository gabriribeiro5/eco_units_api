/* POPULATE DATABASE FOR TESTS AND DEVELOPMENT */

-- ------------------------
-- POPULATING AGENT TABLES
-- ------------------------

-- ----------------
-- INSERT CUSTOMER
-- ----------------
-- 1. Insert agent but do NOT enable
INSERT INTO agent
(`agent_id`,
  `eco_unit_id`,
  `back_user_id`,
  `customer_id`,
  `creation_date_time`,
  `enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled

-- 2. Insert CUSTOMER with agent_id
INSERT INTO customer
(`customer_id`,
`agent_id`,
`customer_name`,
`customer_surname`,
`customer_email`)
VALUES
(DEFAULT,
	(SELECT a.agent_id
	 FROM agent AS a
	 ORDER BY a.creation_date_time DESC
	 LIMIT 1),
"Gabriel",
"Customer da Silva",
"customer_one@gmail.com");

-- 3. Enable last CUSTOMER on AGENT table
UPDATE `ecosystem_db`.`agent`
SET
enabled = 1
WHERE `agent_id` = (SELECT c.agent_id
					FROM customer AS c
                    ORDER BY customer_id DESC
                    LIMIT 1);

-- -----------------
-- INSERT BACK_USER
-- -----------------
-- 1. Insert agent but do NOT enable
INSERT INTO agent
(`agent_id`,
  `eco_unit_id`,
  `back_user_id`,
  `customer_id`,
  `creation_date_time`,
  `enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled

-- 2. Insert BACK_USER with agent_id
INSERT INTO back_user
(`back_user_id`,
`agent_id`,
`name`,
`back_user_surname`,
`back_user_email`)
VALUES
(DEFAULT,
	(SELECT a.agent_id
	 FROM agent AS a
	 ORDER BY a.creation_date_time DESC
	 LIMIT 1),
"Gabriel",
"Worker da Silva",
"back_user_one@gmail.com");

-- 3. Enable last BACK_USER
UPDATE `ecosystem_db`.`agent`
SET
enabled = 1
WHERE `agent_id` = (SELECT b.agent_id
					FROM back_user AS b
                    ORDER BY back_user_id DESC
                    LIMIT 1);

-- ----------------
-- INSERT ECO_UNIT
-- ----------------
-- 1. Insert agent but do NOT enable
INSERT INTO agent
(`agent_id`,
  `eco_unit_id`,
  `back_user_id`,
  `customer_id`,
  `creation_date_time`,
  `enabled`) -- 1 = true
VALUES
(DEFAULT,
NULL,
NULL,
NULL,
CURRENT_TIMESTAMP,
0); -- not enabled

-- 2. Insert ECO_UNIT with agent_id
SELECT * FROM eco_unit;
INSERT INTO `eco_unit`
(`eco_unit_id`,
`agent_id`,
`eco_unit_name`,
`customer_id`,
`ecossys_category_id`,
`require_update`,
`location`,
`deactivated`)
VALUES
(DEFAULT,
	(SELECT a.agent_id
	 FROM agent AS a
	 ORDER BY a.creation_date_time DESC
	 LIMIT 1),
"Lucy",
1, -- ATENTION
3, -- 1 = VEGETABLE GARDEN, 2 = PET HABITAT, 3 = RAINFOREST...
FALSE,
NULL,
FALSE);

-- 3. Enable last ECO_
UPDATE `ecosystem_db`.`agent`
SET
enabled = 1
WHERE `agent_id` = (SELECT e.agent_id
					FROM eco_unit AS b
                    ORDER BY eco_unit_id DESC
                    LIMIT 1);

