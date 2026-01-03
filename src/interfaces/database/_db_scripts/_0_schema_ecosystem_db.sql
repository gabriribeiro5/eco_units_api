-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ecosystem_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ecosystem_db` DEFAULT CHARACTER SET utf8mb4 ;
USE `ecosystem_db` ;

-- -----------------------------------------------------
-- Table `ecosystem_db`.`agent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`agent` (
  `agent_id` INT NOT NULL AUTO_INCREMENT,
  `cyclobot_id` INT NULL,
  `back_user_id` INT NULL,
  `customer_id` INT NULL,
  `creation_date_time` DATETIME NOT NULL,
  PRIMARY KEY (`agent_id`),
  UNIQUE INDEX `cyclobot_id_UNIQUE` (`cyclobot_id` ASC) VISIBLE,
  UNIQUE INDEX `back_user_id_UNIQUE` (`back_user_id` ASC) VISIBLE,
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `customer_name` VARCHAR(100) NOT NULL,
  `customer_surname` VARCHAR(100) NOT NULL,
  `customer_email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `email_UNIQUE` (`customer_email` ASC) INVISIBLE,
  INDEX `customer_email_idx` (`customer_email` ASC) VISIBLE,
  INDEX `customer_name_idx` (`customer_name` ASC, `customer_surname` ASC) VISIBLE,
  INDEX `fk_customer_agent_idx` (`agent_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer_agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = '		';


-- -----------------------------------------------------
-- Table `ecosystem_db`.`ecosystem_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`ecosystem_category` (
  `ecosystem_category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(100) NULL, -- '1 = vegetable garden,\n2 = habitat,\n3 = rainforest,\n4 = swamp,\n5 = prairie',
  `category_description` VARCHAR(200) NULL,
  `min_temperature_expected` INT NULL,
  `max_temperature_expected` INT NULL,
  PRIMARY KEY (`ecosystem_category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`cyclobot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`cyclobot` (
  `cyclobot_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `cyclobot_name` VARCHAR(100) NULL,
  `customer_id` INT NULL,
  `ecosystem_category_id` INT NOT NULL, -- '1 = vegetable garden,\n2 = habitat,\n3 = rainforest,\n4 = savanna,\n5 = desert,\n6 = prairie',
  `require_update` TINYINT NOT NULL, -- 'BOOLEAN. If product config must be updated. 1=YES.',
  `location` GEOMETRY NULL,
  `deactivated` INT NULL,
  PRIMARY KEY (`cyclobot_id`),
  INDEX `fk_cyclobot_customer_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_cyclobot_agent_idx` (`agent_id` ASC) VISIBLE,
  INDEX `fk_cyclobot_ecosystem_category_idx` (`ecosystem_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_cyclobot_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecosystem_db`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cyclobot_agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cyclobot_ecosystem_category`
    FOREIGN KEY (`ecosystem_category_id`)
    REFERENCES `ecosystem_db`.`ecosystem_category` (`ecosystem_category_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = '					';


-- -----------------------------------------------------
-- Table `ecosystem_db`.`back_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`back_user` (
  `back_user_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `back_user_name` VARCHAR(100) NULL,
  `back_user_surname` VARCHAR(100) NULL,
  `back_user_email` VARCHAR(100) NULL,
  PRIMARY KEY (`back_user_id`),
  INDEX `email_idx` (`back_user_email` ASC) INVISIBLE,
  INDEX `name_surname_idx` (`back_user_name` ASC, `back_user_surname` ASC) VISIBLE,
  INDEX `fk_back_user_agent_id_idx` (`agent_id` ASC) INVISIBLE,
  CONSTRAINT `fk_back_user_agent_id`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`agent_input`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`agent_input` (
  `agent_input_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `cyclobot_id` INT NOT NULL,
  `date_time` DATETIME NULL,
  `failed_communication` INT NULL, -- '1 = yes',
  PRIMARY KEY (`agent_input_id`),
  INDEX `fk_agent_input_idx` (`agent_id` ASC) VISIBLE,
  INDEX `fk_agent_input__cyclobot_idx` (`cyclobot_id` ASC) VISIBLE,
  CONSTRAINT `fk_agent_input_back_user`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`back_user` (`agent_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_agent_input_customer`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`customer` (`agent_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_agent_input__cyclobot_by_agent_id`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`cyclobot` (`agent_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_agent_input__cyclobot_by_unit_id`
    FOREIGN KEY (`cyclobot_id`)
    REFERENCES `ecosystem_db`.`cyclobot` (`cyclobot_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`environment_state`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`environment_state` (
  `environment_state_id` INT NOT NULL AUTO_INCREMENT,
  `cyclobot_id` INT NOT NULL,
  `agent_input_id` INT NOT NULL,
  `scan_date_time` DATETIME NULL,
  `soil_moisture` INT NULL,
  `temperature` INT NULL,
  `rain_occurrences_per_day` INT NULL,
  PRIMARY KEY (`environment_state_id`),
  INDEX `fk_environment_state_agent_input_idx` (`agent_input_id` ASC) VISIBLE,
  INDEX `fk_environment_state_agent_input_by_unit_id_idx` (`cyclobot_id` ASC) VISIBLE,
  CONSTRAINT `fk_environment_state_agent_input_by_input_id`
    FOREIGN KEY (`agent_input_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`agent_input_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_environment_state_agent_input_by_unit_id`
    FOREIGN KEY (`cyclobot_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`cyclobot_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`config_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`config_status` (
  `config_status_id` INT NOT NULL,
  `status_name` VARCHAR(45) NOT NULL,
  `status_description` VARCHAR(100) NULL,
  PRIMARY KEY (`config_status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`climate_season`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`climate_season` (
  `climate_season_id` INT NOT NULL,
  `season_name` VARCHAR(45) NULL,
  PRIMARY KEY (`climate_season_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`configuration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`configuration` (
  `configuration_id` INT NOT NULL AUTO_INCREMENT,
  `cyclobot_id` INT NOT NULL,
  `agent_input_id` INT NOT NULL,
  `config_status_id` INT NOT NULL,
  `run_physical_diagnostics` TINYINT NULL,
  `soil_moisture_max` INT NULL,
  `soil_moisture_min` INT NULL,
  `watering_initial_lenght` INT NULL,
  `watering_lenght_growth_rate` INT NULL,
  `watering_lenght_decrease_rate` INT NULL,
  `expected_climate_season` INT NULL,
  PRIMARY KEY (`configuration_id`),
  INDEX `fk_configuration_agent_input_by_unit_id_idx` (`cyclobot_id` ASC) VISIBLE,
  INDEX `fk_configuratin_agent_input_by_input_id_idx` (`agent_input_id` ASC) VISIBLE,
  INDEX `fk_configuratin_config_status_idx` (`config_status_id` ASC) VISIBLE,
  INDEX `fk_configuratin_climate_season_idx` (`expected_climate_season` ASC) VISIBLE,
  CONSTRAINT `fk_configuration_agent_input_by_unit_id`
    FOREIGN KEY (`cyclobot_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`cyclobot_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_configuratin_agent_input_by_input_id`
    FOREIGN KEY (`agent_input_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`agent_input_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_configuratin_config_status`
    FOREIGN KEY (`config_status_id`)
    REFERENCES `ecosystem_db`.`config_status` (`config_status_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_configuratin_climate_season`
    FOREIGN KEY (`expected_climate_season`)
    REFERENCES `ecosystem_db`.`climate_season` (`climate_season_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`sensor_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`sensor_status` (
  `sensor_status_id` SMALLINT NOT NULL,
  `sensor_status_name` VARCHAR(45) NOT NULL,
  `sensor_status_description` VARCHAR(200) NULL,
  PRIMARY KEY (`sensor_status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecosystem_db`.`diagnostic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`diagnostic` (
  `diagnostic_id` INT NOT NULL AUTO_INCREMENT,
  `cyclobot_id` INT NOT NULL,
  `agent_input_id` INT NOT NULL,
  `diagnostic_date_time` DATETIME NULL,
  `cyclobot_message` VARCHAR(200) NULL,
  `wifi_connected` SMALLINT NOT NULL,
  `watering_system` SMALLINT NOT NULL,
  `river_system` SMALLINT NOT NULL,
  `wind_system` SMALLINT NOT NULL,
  `lighting_system` SMALLINT NOT NULL,
  PRIMARY KEY (`diagnostic_id`),
  INDEX `fk_diagnostic_agent_input_by_input_id_idx` (`agent_input_id` ASC) VISIBLE,
  INDEX `fk_diagnostic_agent_input_by_unit_id_idx` (`cyclobot_id` ASC) VISIBLE,
  INDEX `fk_diagnostic_sensor_status_idx` (`wifi_connected` ASC) VISIBLE,
  CONSTRAINT `fk_diagnostic_agent_input_by_input_id`
    FOREIGN KEY (`agent_input_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`agent_input_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_diagnostic_agent_input_by_unit_id`
    FOREIGN KEY (`cyclobot_id`)
    REFERENCES `ecosystem_db`.`agent_input` (`cyclobot_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_diagnostic_sensor_status_wifi_connected`
    FOREIGN KEY (`wifi_connected`)
    REFERENCES `ecosystem_db`.`sensor_status` (`sensor_status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;