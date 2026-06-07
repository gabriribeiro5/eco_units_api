-- select device_operation_supervisor by email
SELECT *
FROM `device_operation_supervisor`
WHERE `device_operation_supervisor_email` = %s