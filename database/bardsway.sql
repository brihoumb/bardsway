CREATE DATABASE IF NOT EXISTS bard_storage;
USE bard_storage;

CREATE TABLE IF NOT EXISTS `results` (
	`id` INT NOT NULL auto_increment,
	`music_name` LONGTEXT,
	`total_notes` INT,
	`correct_notes` INT,
	`score_max` INT,
	`score` INT,
	`id_battery` INT,
	PRIMARY KEY( `id` )
);

CREATE TABLE IF NOT EXISTS `musics` (
	`id` INT NOT NULL auto_increment,
	`music_path` LONGTEXT,
	PRIMARY KEY( `id` )
);
