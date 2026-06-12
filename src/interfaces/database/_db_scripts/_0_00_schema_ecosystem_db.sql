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
-- -----------------------------------------------------
-- ----------------- AUTHENTICATION --------------------
-- -----------------------------------------------------
-- -----------------------------------------------------

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`agent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`agent` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`agent` (
  `agent_id` INT NOT NULL AUTO_INCREMENT,
  `backoffice_admin_id` INT NULL,
  `device_operation_agent_id` INT NULL,
  `supply_chain_manager_id` INT NULL,
  `creation_date_time` DATETIME NOT NULL,
  `is_enabled` TINYINT NOT NULL,
  PRIMARY KEY (`agent_id`),
  UNIQUE INDEX `idx_UNIQUE_backoffice_admin_id` (`backoffice_admin_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_device_operation_agent_id` (`device_operation_agent_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_supply_chain_manager_id` (`supply_chain_manager_id` ASC) VISIBLE,
  CONSTRAINT `fk_agent__backoffice_admin`
    FOREIGN KEY (`backoffice_admin_id`)
    REFERENCES `ecosystem_db`.`backoffice_admin` (`backoffice_admin_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_agent__device_operation_agent`
    FOREIGN KEY (`device_operation_agent_id`)
    REFERENCES `ecosystem_db`.`device_operation_agent` (`device_operation_agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_agent__supply_chain_manager`
    FOREIGN KEY (`supply_chain_manager_id`)
    REFERENCES `ecosystem_db`.`supply_chain_manager` (`manager_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AUTHENTICATION Table `ecosystem_db`.`first_auth_agent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`first_auth_agent` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`first_auth_agent` (
  `agent_id` INT NOT NULL,
  `token` VARCHAR(45) NOT NULL,
  `max_lenght_first_auth` INT NULL,
  PRIMARY KEY (`agent_id`),
  INDEX `idx_agent_id` (`agent_id` ASC) VISIBLE,
  CONSTRAINT `fk_first_auth__agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AUTHENTICATION Table `ecosystem_db`.`session`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`session` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`session` (
  `agent_id` INT NOT NULL,
  `token` VARCHAR(45) NOT NULL,
  `max_lenght_session` INT NULL, -- Drop session if it lasts more than this value in seconds. Null means no limit.
  PRIMARY KEY (`agent_id`),
  INDEX `idx_agent_id` (`agent_id` ASC) VISIBLE,
  CONSTRAINT `fk_session__agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- -----------------------------------------------------
-- ---------------------- AGENT ------------------------
-- -----------------------------------------------------
-- -----------------------------------------------------

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`backoffice_admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`backoffice_admin` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`backoffice_admin` (
  `backoffice_admin_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `backoffice_admin_email` VARCHAR(100) UNIQUE NOT NULL,
  `backoffice_admin_name` VARCHAR(100) NOT NULL,
  `backoffice_admin_surname` VARCHAR(100) NOT NULL,
  `backoffice_admin_secret` VARCHAR(100) NOT NULL, -- This is used for session communication. The actual device secret is not stored in the database, only its encrypted version.
  PRIMARY KEY (`backoffice_admin_id`),
  UNIQUE INDEX `idx_UNIQUE_agent_id` (`agent_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_backoffice_admin_email` (`backoffice_admin_email` ASC) VISIBLE,
  CONSTRAINT `fk_backoffice_admin__agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`device_operation_agent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_operation_agent` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_operation_agent` (
  `device_operation_agent_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `supervisor_id` INT NULL,
  `device_id` INT NULL,
  `customer_id` INT NULL,
  `creation_date_time` DATETIME NOT NULL,
  PRIMARY KEY (`device_operation_agent_id`),
  UNIQUE INDEX `idx_UNIQUE_agent_id` (`agent_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_supervisor_id` (`supervisor_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_device_id` (`device_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_customer_id` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_device_operation_agent__agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_operation_agent__device_operation_supervisor`
    FOREIGN KEY (`supervisor_id`)
    REFERENCES `ecosystem_db`.`device_operation_supervisor` (`device_operation_supervisor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_operation_agent__device`
    FOREIGN KEY (`device_id`)
    REFERENCES `ecosystem_db`.`device` (`device_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_operation_agent__customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecosystem_db`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`device_operation_supervisor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_operation_supervisor` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_operation_supervisor` (
  `device_operation_supervisor_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_agent_id` INT NOT NULL,
  `device_operation_supervisor_email` VARCHAR(100) UNIQUE NOT NULL,
  `device_operation_supervisor_name` VARCHAR(100) NOT NULL,
  `device_operation_supervisor_surname` VARCHAR(100) NOT NULL,
  `device_operation_supervisor_secret` VARCHAR(100) NOT NULL, -- This is used for session communication. The actual device secret is not stored in the database, only its encrypted version.
  PRIMARY KEY (`device_operation_supervisor_id`),
  UNIQUE INDEX `idx_UNIQUE_device_operation_agent_id` (`device_operation_agent_id` ASC) INVISIBLE,
  UNIQUE INDEX `idx_UNIQUE_device_operation_supervisor_email` (`device_operation_supervisor_email` ASC) INVISIBLE,
  CONSTRAINT `fk_device_operation_supervisor__device_operation_agent`
    FOREIGN KEY (`device_operation_agent_id`)
    REFERENCES `ecosystem_db`.`device_operation_agent` (`device_operation_agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`sales_service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`sales_service` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`sales_service` (
  `sales_service_id` INT NOT NULL AUTO_INCREMENT,
  `sales_service_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`sales_service_id`)
)
ENGINE = InnoDB;

-- -- -----------------------------------------------------
-- -- AGENT Table `ecosystem_db`.`customer`
-- -- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`customer` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `sales_service_id` INT NULL,
  `device_operation_agent_id` INT NOT NULL,
  `customer_email` VARCHAR(100) UNIQUE NOT NULL,
  `customer_name` VARCHAR(100) NOT NULL,
  `customer_surname` VARCHAR(100) NOT NULL,
  `customer_secret` VARCHAR(100) NOT NULL, -- This is used for session communication. The actual device secret is not stored in the database, only its encrypted version.
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `idx_UNIQUE_device_operation_agent_id` (`device_operation_agent_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_customer_email` (`customer_email` ASC) VISIBLE,
  INDEX `idx_sales_service_id` (`sales_service_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer__sales_service`
    FOREIGN KEY (`sales_service_id`)
    REFERENCES `ecosystem_db`.`sales_service` (`sales_service_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_customer__device_operation_agent`
    FOREIGN KEY (`device_operation_agent_id`)
    REFERENCES `ecosystem_db`.`device_operation_agent` (`device_operation_agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
COMMENT = '		';

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`supply_chain_manager`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain_manager` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain_manager` (
  `manager_id` INT NOT NULL AUTO_INCREMENT,
  `agent_id` INT NOT NULL,
  `manager_email` VARCHAR(100) NOT NULL,
  `manager_name` VARCHAR(100) NOT NULL,
  `manager_surname` VARCHAR(100) NOT NULL,
  `manager_secret` VARCHAR(100) NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE INDEX `idx_UNIQUE_agent_id` (`agent_id` ASC) VISIBLE,
  UNIQUE INDEX `idx_UNIQUE_manager_email` (`manager_email` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain_manager__agent`
    FOREIGN KEY (`agent_id`)
    REFERENCES `ecosystem_db`.`agent` (`agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`supply_chain`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain` (
  `supply_chain_id` INT NOT NULL AUTO_INCREMENT,
  `created_by_manager_id` INT NOT NULL,
  `created_at_date_time` DATETIME NULL,
  `updated_by_manager_id` INT NULL,
  `last_update_date_time` DATETIME NULL,
  `partner_list_id_for_consulting` INT NULL, -- architect, engineer, ecology specialist, project management, finance, law, etc
  `partner_list_id_for_regulatory` INT NULL, -- government and regulatory bodies, including certification and compliance specialists
  `partner_list_id_for_product_design` INT NULL, -- 3D designer, UX designer
  `partner_list_id_for_customer_service` INT NULL, -- customer and warranty service, etc
  `partner_list_id_for_advertising` INT NULL, -- frontend, social media, etc
  `partner_list_id_for_sales` INT NULL, -- ecommerce, retail, etc
  `partner_list_id_for_software` INT NULL, -- software provider, including firmware, app, and cloud software
  `partner_list_id_for_electronics` INT NULL, -- electronics supplier
  `partner_list_id_for_blacksmith` INT NULL, -- metal parts supplier
  `partner_list_id_for_glass_shop` INT NULL, -- glass box supplier
  `partner_list_id_for_carpentry` INT NULL, -- wood parts supplier
  `partner_list_id_for_natural_materials` INT NULL, -- natural materials supplier
  `partner_list_id_for_operational` INT NULL, -- supply chain management and product montage specialist
  `partner_list_id_for_logistics` INT NULL, -- logistics provider
  `partner_list_id_for_installation` INT NULL, -- installation specialist
  `partner_list_id_for_maintenance` INT NULL, -- maintenance specialist
  PRIMARY KEY (`supply_chain_id`),
  INDEX `idx_created_by_manager_id` (`created_by_manager_id` ASC) VISIBLE,
  INDEX `idx_updated_by_manager_id` (`updated_by_manager_id` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain__supply_chain_manager_created_by`
    FOREIGN KEY (`created_by_manager_id`)
    REFERENCES `ecosystem_db`.`supply_chain_manager` (`manager_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_supply_chain__supply_chain_manager_updated_by`
    FOREIGN KEY (`updated_by_manager_id`)
    REFERENCES `ecosystem_db`.`supply_chain_manager` (`manager_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
COMMENT = '	Once appproved, a supply chain is created for a device model and can NOT be updated (only deleted). 
 Each supply chain has a list of partners for each category. \n
 When an order is made, the supply chain details are copied to the order, so the order can be fulfilled even if the supply chain changes later.';


-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`chart`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`chart` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`chart` (
  `chart_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `creation_date_time` DATETIME NOT NULL,
  `dict_device_model_id_and_quantity` VARCHAR(255) NULL, -- Dict of device models and quantities included in the chart. Null means no device models.
  PRIMARY KEY (`chart_id`),
  INDEX `idx_UNIQUE_customer_id` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_chart__customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecosystem_db`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`payment_method`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`payment_method` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`payment_method` (
  `payment_method_id` INT NOT NULL AUTO_INCREMENT,
  `payment_method_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`payment_method_id`)
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`payment_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`payment_status` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`payment_status` (
  `payment_status_id` INT NOT NULL AUTO_INCREMENT,
  `payment_status_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`payment_status_id`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`payment` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`payment` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `chart_id` INT NOT NULL,
  `payment_method_id` INT NOT NULL,
  `payment_status_id` INT NOT NULL,
  `payment_amount` INT NOT NULL,
  `creation_date` DATE NOT NULL,
  `last_update_date` DATE NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `idx_UNIQUE_chart_id` (`chart_id` ASC) VISIBLE,
  INDEX `idx_UNIQUE_payment_method_id` (`payment_method_id` ASC) VISIBLE,
  INDEX `idx_UNIQUE_payment_status_id` (`payment_status_id` ASC) VISIBLE,
  CONSTRAINT `fk_payment__chart`
    FOREIGN KEY (`chart_id`)
    REFERENCES `ecosystem_db`.`chart` (`chart_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_payment__payment_method`
    FOREIGN KEY (`payment_method_id`)
    REFERENCES `ecosystem_db`.`payment_method` (`payment_method_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_payment__payment_status`
    FOREIGN KEY (`payment_status_id`)
    REFERENCES `ecosystem_db`.`payment_status` (`payment_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`device_strategy`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_strategy` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_strategy` (
  `device_strategy_id` INT NOT NULL AUTO_INCREMENT,
  `strategy_compact_name` INT NOT NULL,
  `strategy_full_name` VARCHAR(100) NOT NULL,
  `strategy_description` VARCHAR(200) NULL,
  `min_temperature_expected` INT NULL,
  `max_temperature_expected` INT NULL,
  PRIMARY KEY (`device_strategy_id`),
  UNIQUE INDEX `idx_UNIQUE_strategy_compact_name` (`strategy_compact_name` ASC) VISIBLE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`device_model`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_model` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_model` (
  `device_model_id` INT NOT NULL AUTO_INCREMENT,
  `supply_chain_id` INT NOT NULL,
  `list_id_for_authorized_sales_services` INT NULL, -- Null means all sales services are authorized.
  `model_name` VARCHAR(100) NOT NULL,
  `model_description` VARCHAR(200) NULL,
  `consulting_services_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `regulatory_compliance_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `product_design_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `customer_service_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `advertising_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `sales_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `software_cost` INT NULL, -- Including service fee over software management and maintenance. Null means not defined.
  `electronics_cost` INT NULL, -- Including service fee over hardware management, installation, and maintenance. Null means not defined.
  `box_cost` INT NULL, -- glass box cost
  `landscape_cost` INT NULL, -- manly natural materials and landscaping cost
  `operational_cost` INT NULL, -- including service fee over hardware management, installation, and maintenance. Null means not defined.
  `logistics_cost` INT NULL,
  `installation_cost` INT NULL,
  `maintenance_cost` INT NULL,
  `total_price` INT NULL,
  `monthly_fee` INT NULL,
  `annual_fee` INT NULL,
  PRIMARY KEY (`device_model_id`),
  INDEX `idx_UNIQUE_supply_chain_id` (`supply_chain_id` ASC) VISIBLE,
  INDEX `idx_UNIQUE_list_id_for_authorized_sales_services` (`list_id_for_authorized_sales_services` ASC) VISIBLE,
  CONSTRAINT `fk_device_model_supply_chain`
    FOREIGN KEY (`supply_chain_id`)
    REFERENCES `ecosystem_db`.`supply_chain` (`supply_chain_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`device_position`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_position` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_position` (
  `device_position_id` INT NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(45) NOT NULL, -- `waiting supply chain`, `stocked`, `transport to customer`, `delivered`
  `status_description` VARCHAR(200) NULL,
  PRIMARY KEY (`device_position_id`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- AGENT Table `ecosystem_db`.`device`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device` (
  `device_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_agent_id` INT NOT NULL,
  `device_strategy_id` INT NOT NULL,
  `device_model_id` INT NOT NULL,
  `device_position_id` INT NOT NULL,
  `sold_at` DATETIME NULL,
  `customer_id` INT NULL,
  `updated_by_device_operation_supervisor_id` INT NULL,
  `updated_at` DATETIME NOT NULL,
  `require_config_update` TINYINT NOT NULL, -- BOOLEAN. If product config must be updated. 1=YES. - this triggers device update mode, use carefully.
  `require_firmware_update` TINYINT NOT NULL, -- BOOLEAN. If product firmware must be updated. 1=YES. - this triggers device update mode, use carefully.
  `device_secret` VARCHAR(100) NOT NULL, -- This is used for session communication. The actual device secret is not stored in the database, only its encrypted version.
  `device_name` VARCHAR(100) NULL,
  `location` GEOMETRY NULL,
  `max_input_hertz` INT NULL,  -- Drop device_operation if it exceeds this value in a second. Null means no limit.
  PRIMARY KEY (`device_id`),
  UNIQUE INDEX `idx_UNIQUE_device_operation_agent_id` (`device_operation_agent_id` ASC) VISIBLE,
  INDEX `idx_device_strategy_id` (`device_strategy_id` ASC) VISIBLE,
  INDEX `idx_device_model_id` (`device_model_id` ASC) VISIBLE,
  INDEX `idx_customer_id` (`customer_id` ASC) VISIBLE,
  INDEX `idx_device_operation_supervisor_update_id` (`updated_by_device_operation_supervisor_id` ASC) VISIBLE,
  INDEX `idx_device_position_id` (`device_position_id` ASC) VISIBLE,
  CONSTRAINT `fk_device__device_operation_agent`
    FOREIGN KEY (`device_operation_agent_id`)
    REFERENCES `ecosystem_db`.`device_operation_agent` (`device_operation_agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_device_strategy`
    FOREIGN KEY (`device_strategy_id`)  
    REFERENCES `ecosystem_db`.`device_strategy` (`device_strategy_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_device_model`
    FOREIGN KEY (`device_model_id`)
    REFERENCES `ecosystem_db`.`device_model` (`device_model_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecosystem_db`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_device_operation_supervisor_update`
    FOREIGN KEY (`updated_by_device_operation_supervisor_id`)
    REFERENCES `ecosystem_db`.`device_operation_supervisor` (`device_operation_supervisor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_device_position`
    FOREIGN KEY (`device_position_id`)
    REFERENCES `ecosystem_db`.`device_position` (`device_position_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
COMMENT = '        ';

-- -- -----------------------------------------------------
-- -- -----------------------------------------------------
-- -- ----------------- DEVICE OPERATION ------------------
-- -- -----------------------------------------------------
-- -- -----------------------------------------------------

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`device_operation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_operation` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_operation` (
  `device_operation_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_agent_id` INT NOT NULL,
  `device_id` INT NOT NULL,
  `date_time` DATETIME NULL,
  `operation_type` INT NULL, -- '1 = insert, 2 = update, 3 = delete',
  PRIMARY KEY (`device_operation_id`),
  INDEX `idx_device_operation_agent_id` (`device_operation_agent_id` ASC) VISIBLE,
  INDEX `idx_device_id` (`device_id` ASC) VISIBLE,
  CONSTRAINT `fk_device_operation__device_operation_agent`
    FOREIGN KEY (`device_operation_agent_id`)
    REFERENCES `ecosystem_db`.`device_operation_agent` (`device_operation_agent_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_device_operation__device`
    FOREIGN KEY (`device_id`)
    REFERENCES `ecosystem_db`.`device` (`device_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- DEVICE OPERATION Table `ecosystem_db`.`ecosystem_state`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`ecosystem_state` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`ecosystem_state` (
  `ecosystem_state_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_id` INT NOT NULL,
  `scan_date_time` DATETIME NULL,
  `soil_moisture` INT NULL,
  `temperature` INT NULL,
  `rain_occurrences_per_day` INT NULL,
  PRIMARY KEY (`ecosystem_state_id`),
  UNIQUE INDEX `idx_device_operation_id` (`device_operation_id` ASC) VISIBLE,
  CONSTRAINT `fk_ecosystem_state__device_operation`
    FOREIGN KEY (`device_operation_id`)
    REFERENCES `ecosystem_db`.`device_operation` (`device_operation_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`config_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`config_status` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`config_status` (
  `config_status_id` INT NOT NULL,
  `status_name` VARCHAR(45) NOT NULL,
  `status_description` VARCHAR(100) NULL,
  PRIMARY KEY (`config_status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`climate_season`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`climate_season` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`climate_season` (
  `climate_season_id` INT NOT NULL,
  `season_name` VARCHAR(45) NULL,
  PRIMARY KEY (`climate_season_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- DEVICE OPERATION Table `ecosystem_db`.`device_configuration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`device_configuration` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`device_configuration` (
  `configuration_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_id` INT NOT NULL,
  `config_status_id` INT NOT NULL,
  `expected_climate_season_id` INT NULL,
  `run_physical_diagnostics` TINYINT NULL,
  `limits_dict_for_soil_moisture` VARCHAR(255) NULL,
  `limits_dict_for_soil_temperature` VARCHAR(255) NULL,
  `limits_dict_for_air_humidity` VARCHAR(255) NULL,
  `limits_dict_for_light_intensity` VARCHAR(255) NULL,
  `limits_dict_for_rain_occurrences` VARCHAR(255) NULL,
  `limits_dict_for_temperature` VARCHAR(255) NULL,
  `params_dict_for_watering` VARCHAR(255) NULL,
  `params_dict_for_fan` VARCHAR(255) NULL,
  `params_dict_for_lighting` VARCHAR(255) NULL,
  `params_dict_for_filtering` VARCHAR(255) NULL,
  `params_dict_for_cleaning` VARCHAR(255) NULL,
  PRIMARY KEY (`configuration_id`),
  INDEX `idx_device_operation_id` (`device_operation_id` ASC) VISIBLE,
  INDEX `idx_config_status_id` (`config_status_id` ASC) VISIBLE,
  INDEX `idx_expected_climate_season_id` (`expected_climate_season_id` ASC) VISIBLE,
  CONSTRAINT `fk_configuratin_device_operation_by_input_id`
    FOREIGN KEY (`device_operation_id`)
    REFERENCES `ecosystem_db`.`device_operation` (`device_operation_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_configuratin_config_status`
    FOREIGN KEY (`config_status_id`)
    REFERENCES `ecosystem_db`.`config_status` (`config_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_configuratin_climate_season`
    FOREIGN KEY (`expected_climate_season_id`)
    REFERENCES `ecosystem_db`.`climate_season` (`climate_season_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`component_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`component_status` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`component_status` (
  `component_status_id` SMALLINT NOT NULL,
  `component_status_name` VARCHAR(45) NOT NULL,
  `component_status_description` VARCHAR(200) NULL,
  PRIMARY KEY (`component_status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- DEVICE OPERATION Table `ecosystem_db`.`diagnostic`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`diagnostic` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`diagnostic` (
  `diagnostic_id` INT NOT NULL AUTO_INCREMENT,
  `device_operation_id` INT NOT NULL,
  `diagnostic_date_time` DATETIME NULL,
  `device_message` VARCHAR(200) NULL,
  `sensor_status_all_components` SMALLINT NULL,
  `sensor_status_soil_moisture` SMALLINT NULL,
  `sensor_status_soil_temperature` SMALLINT NULL,
  `sensor_status_air_humidity` SMALLINT NULL,
  `sensor_status_light_intensity` SMALLINT NULL,
  `sensor_status_rain_occurrences` SMALLINT NULL,
  `sensor_status_temperature` SMALLINT NULL,
  `actuator_status_all_components` SMALLINT NULL,
  `actuator_status_watering` SMALLINT NULL,
  `actuator_status_fan` SMALLINT NULL,
  `actuator_status_lighting` SMALLINT NULL,
  `actuator_status_filtering` SMALLINT NULL,
  `actuator_status_cleaning` SMALLINT NULL,
  PRIMARY KEY (`diagnostic_id`),
  INDEX `idx_device_operation_id` (`device_operation_id` ASC) VISIBLE,
  CONSTRAINT `fk_diagnostic__device_operation`
    FOREIGN KEY (`device_operation_id`)
    REFERENCES `ecosystem_db`.`device_operation` (`device_operation_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_diagnostic__component_status_sensor_soil_moisture`
    FOREIGN KEY (`sensor_status_all_components`)
    REFERENCES `ecosystem_db`.`component_status` (`component_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_diagnostic__component_status_actuator_watering`
    FOREIGN KEY (`actuator_status_all_components`)
    REFERENCES `ecosystem_db`.`component_status` (`component_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) 
ENGINE = InnoDB;



-- -- -----------------------------------------------------
-- -- -----------------------------------------------------
-- -- -------------- SUPPLY CHAIN OPERATION --------------
-- -- -----------------------------------------------------
-- -- -----------------------------------------------------

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`supply_chain_partner_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain_partner_category` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain_partner_category` (
  `partner_category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(100) NOT NULL, -- consulting,\n product_design,\n customer_service,\n advertising,\n sales,\n software,\n electronics,\n blacksmith,\n glass_shop,\n carpentry,\n natural_materials,\n montage,\n logistics,\n installation,\n maintenance
  `category_description` VARCHAR(200) NULL,
  PRIMARY KEY (`partner_category_id`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- REQUIRED Table `ecosystem_db`.`supply_chain_partner`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain_partner` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain_partner` (
  `supply_chain_partner_id` INT NOT NULL AUTO_INCREMENT,
  `partner_category_id` INT NULL,
  `partner_company_name` VARCHAR(100) NOT NULL,
  `partner_company_cnpj` VARCHAR(50) NOT NULL,
  `partner_address` VARCHAR(100) NOT NULL,
  `partner_CEP` VARCHAR(50) NOT NULL,
  `partner_sellesperson_email` VARCHAR(100) NULL,
  `partner_sellesperson_name` VARCHAR(100) NULL,
  `partner_sellesperson_phone` VARCHAR(100) NULL,
  `partner_curstomer_service_email` VARCHAR(100) NULL,
  `partner_curstomer_service_name` VARCHAR(100) NULL,
  `partner_curstomer_service_phone` VARCHAR(100) NULL,
  `partner_owner_email` VARCHAR(100) NULL,
  `partner_owner_name` VARCHAR(100) NULL,
  `partner_owner_phone` VARCHAR(100) NULL,
  `partner_dependency_layer` INT NOT NULL, -- '0 = serves to me,\n1 = serves to my supplier,\n2 = serves to my supplier's supplier, \n3 = primary source',
  `partner_position_in_chain` VARCHAR(200) NULL, -- 
  PRIMARY KEY (`supply_chain_partner_id`),
  INDEX `idx_partner_category_id` (`partner_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain_partner__supply_chain_partner_category`
    FOREIGN KEY (`partner_category_id`)
    REFERENCES `ecosystem_db`.`supply_chain_partner_category` (`partner_category_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- SUPPLY CHAIN OPERATION Table `ecosystem_db`.`order_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`order_status` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`order_status` (
  `order_status_id` INT NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(45) NOT NULL, -- 'cancelled, waiting components, montage, transport, feedback received'
  PRIMARY KEY (`order_status_id`)
)
ENGINE = InnoDB;

-- SUPPLY CHAIN OPERATION Table `ecosystem_db`.`supply_chain_order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain_order` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain_order` (
  `supply_chain_order_id` INT NOT NULL AUTO_INCREMENT,
  `device_id` INT NOT NULL,
  `order_date_time` DATETIME NULL,
  `order_status_id` INT NULL, -- 'cancelled, waiting components, montage, transport, feedback received'
  `order_total_price` INT NULL,
  PRIMARY KEY (`supply_chain_order_id`),
  INDEX `idx_device_id` (`device_id` ASC) VISIBLE,
  INDEX `idx_order_status_id` (`order_status_id` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain_order__device`
    FOREIGN KEY (`device_id`)
    REFERENCES `ecosystem_db`.`device` (`device_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_supply_chain_order__order_status`
    FOREIGN KEY (`order_status_id`)
    REFERENCES `ecosystem_db`.`order_status` (`order_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- SUPPLY CHAIN OPERATION Table `ecosystem_db`.`suborder_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`suborder_status` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`suborder_status` (
  `suborder_status_id` INT NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(45) NOT NULL, -- 'created, cancelled, sent, confirmed, operational, transport, received'
  PRIMARY KEY (`suborder_status_id`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- SUPPLY CHAIN OPERATION Table `ecosystem_db`.`supply_chain_suborder`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ecosystem_db`.`supply_chain_suborder` ;
CREATE TABLE IF NOT EXISTS `ecosystem_db`.`supply_chain_suborder` (
  `supply_chain_suborder_id` INT NOT NULL AUTO_INCREMENT,
  `supply_chain_order_id` INT NOT NULL,
  `supply_chain_partner_id` INT NOT NULL,
  `suborder_status_id` INT NOT NULL, -- 'created, cancelled, sent, confirmed, operational, transport, received'
  `suborder_date_time` DATETIME NOT NULL,
  `promised_delivery_date_time` DATETIME NULL,
  `actual_delivery_date_time` DATETIME NULL,
  `suborder_total_price` INT NULL,
  PRIMARY KEY (`supply_chain_suborder_id`),
  INDEX `idx_supply_chain_order_id` (`supply_chain_order_id` ASC) VISIBLE,
  INDEX `idx_suborder_status_id` (`suborder_status_id` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain_suborder__supply_chain_order`
    FOREIGN KEY (`supply_chain_order_id`)
    REFERENCES `ecosystem_db`.`supply_chain_order` (`supply_chain_order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  INDEX `idx_supply_chain_partner_id` (`supply_chain_partner_id` ASC) VISIBLE,
  CONSTRAINT `fk_supply_chain_suborder__supply_chain_partner`
    FOREIGN KEY (`supply_chain_partner_id`)
    REFERENCES `ecosystem_db`.`supply_chain_partner` (`supply_chain_partner_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_supply_chain_suborder__suborder_status`
    FOREIGN KEY (`suborder_status_id`)
    REFERENCES `ecosystem_db`.`suborder_status` (`suborder_status_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;