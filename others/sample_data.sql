INSERT INTO `car_frame` (id, name) 
    VALUES (NULL, 'Salon'), (NULL, 'Micro'), (NULL, 'Sedan'), (NULL, 'CUV'), (NULL, 'SUV'), (NULL, 'Mini Truck'), (NULL, 'Minivan');
INSERT INTO `damagetype` (id, code, description) 
    VALUES (NULL, 'A1', 'Small Scratch'), (NULL, 'A2', 'Scratch'), (NULL, 'A3', 'Big Scratch'), (NULL, 'E1', 'Few Dimples'), (NULL, 'E2', 'Several Dimples');
INSERT INTO `frame_components` (id, frame_id, component) 
    VALUES (NULL, '1', 'Back Mirror'), (NULL, '1', 'Front Mirror'), (NULL, '1', 'Right Mirror'), (NULL, '1', 'Left Mirror');
INSERT INTO `employees` (`id`, `name`, `position`, `username`, `password`, `hidden`) 
    VALUES (NULL, 'admin', 'admin', 'admin', 'admin', '0'),(NULL, 'employee', 'employee', 'employee', 'employee', '0');
INSERT INTO 'google_cred' ('id','token','refresh_token','token_uri','client_id','client_secret','scopes')
    VALUES (NULL,'ya29.a0AX9GBdUVjQbRhXuZe6d0n2adN_zBjxjCqWvpiyss9cqsk_8hxuXTA1JjIjMWOz3yKFCfKvpZMRz-FhISktHdZd-ENul2vM0sFl8SWEdBK7aFod6QBHE7GBMoxN84AjEXvFasCVKT_zUtOHIoLJqAb_mYRJlcaCgYKAWoSARASFQHUCsbCxW0BU5-tLx3qFZN5FgOveQ0163','1//0dcajgDEm3DNyCgYIARAAGA0SNwF-L9IrQb1-bVJ5pMzS3H9LGF_0Upb5jyQW9QNQcU9dw3ZTVFyk2AYa5oy34NSOS-S-N7bPOMk','https://oauth2.googleapis.com/token','298695646965-k8h2b7c1p8nn92j2b0mbuca954fmv1g6.apps.googleusercontent.com','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','https://www.googleapis.com/auth/drive');