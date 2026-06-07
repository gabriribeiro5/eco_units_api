-- select device_operation_supervisor admin by email
SELECT *
FROM `backoffice_admin`
WHERE `backoffice_admin_email` = %s