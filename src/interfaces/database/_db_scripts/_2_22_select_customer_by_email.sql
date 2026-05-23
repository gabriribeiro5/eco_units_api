-- select customer by email
SELECT *
FROM `customers`
WHERE `backuser_admin_email` = %s