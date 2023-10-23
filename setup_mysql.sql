-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS afriheal;
CREATE USER IF NOT EXISTS 'saisa'@'localhost' IDENTIFIED BY 'sais_dev_pwd';
GRANT ALL PRIVILEGES ON `afriheal`.* TO 'saisa'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'saisa'@'localhost';
FLUSH PRIVILEGES;
