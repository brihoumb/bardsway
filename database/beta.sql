CREATE DATABASE IF NOT EXISTS bardsway;
USE bardsway;

CREATE TABLE IF NOT EXISTS beta (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(320),
    `software` VARCHAR(20),
    `platform` VARCHAR(8),
    `topic` VARCHAR(10),
    `other` VARCHAR(256),
    `message` VARCHAR(8192),
    `screenshots` JSON,
    PRIMARY KEY(`id`)
);
