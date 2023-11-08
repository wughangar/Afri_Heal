DROP DATABASE IF EXISTS afriheal;
CREATE DATABASE IF NOT EXISTS afriheal;
CREATE USER IF NOT EXISTS 'LOKI'@'localhost' IDENTIFIED BY 'loki_pwd';
GRANT USAGE ON *.* TO 'LOKI'@'localhost';
GRANT ALL PRIVILEGES ON  `afriheal`.* TO 'LOKI'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'LOKI'@'localhost';
USE afriheal;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    phone INT NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL
);
CREATE TABLE therapists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    phone INT NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    specialization VARCHAR(128) NOT NULL,
    experience VARCHAR(128) NOT NULL,
    availability BOOLEAN NOT NULL DEFAULT 1
);
ALTER TABLE therapists
ADD COLUMN created_at DATETIME DEFAULT NOW(),
ADD COLUMN updated_at DATETIME DEFAULT NOW();
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(60),
    therapist_id VARCHAR(60),
    rating INT,
    date DATETIME,
    comments VARCHAR(1024),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
