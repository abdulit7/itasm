# import mysql.connector

# def recreate_database():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Drop existing tables individually (adjusted order to handle foreign key constraints)
#         drop_statements = [
#             "DROP TABLE IF EXISTS asset_history;",
#             "DROP TABLE IF EXISTS asset_bills;",
#             "DROP TABLE IF EXISTS asset_images;",
#             "DROP TABLE IF EXISTS job_cards;",  # Drop job_cards first due to asset_id foreign key
#             "DROP TABLE IF EXISTS assets;",
#             "DROP TABLE IF EXISTS device_bills;",
#             "DROP TABLE IF EXISTS device_images;",
#             "DROP TABLE IF EXISTS devices;",
#             "DROP TABLE IF EXISTS component_bills;",
#             "DROP TABLE IF EXISTS component_images;",
#             "DROP TABLE IF EXISTS components;",
#             "DROP TABLE IF EXISTS category;",
#             "DROP TABLE IF EXISTS users;",
#             "DROP TABLE IF EXISTS department;"
#         ]
#         for statement in drop_statements:
#             cursor.execute(statement)

#         # Create department table
#         create_department_table = """
#         CREATE TABLE department (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_department_table)

#         # Create users table
#         create_users_table = """
#         CREATE TABLE users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             emp_id VARCHAR(50) NOT NULL UNIQUE,
#             password VARCHAR(255),
#             branch VARCHAR(100) NOT NULL,
#             department_id INT NOT NULL,
#             can_login TINYINT(1) DEFAULT 0,
#             image_path VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_users_table)

#         # Create category table
#         create_category_table = """
#         CREATE TABLE category (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             type VARCHAR(50) NOT NULL,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_category_table)

#         # Create components table
#         create_components_table = """
#         CREATE TABLE components (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             category_id INT,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_asset VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_components_table)

#         # Create component_images table
#         create_component_images_table = """
#         CREATE TABLE component_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_images_table)

#         # Create component_bills table
#         create_component_bills_table = """
#         CREATE TABLE component_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_bills_table)

#         # Create devices table
#         create_devices_table = """
#         CREATE TABLE devices (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             distributor_name VARCHAR(255),
#             distributor_location VARCHAR(255),
#             device_tag VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_devices_table)

#         # Create device_images table
#         create_device_images_table = """
#         CREATE TABLE device_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_images_table)

#         # Create device_bills table
#         create_device_bills_table = """
#         CREATE TABLE device_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_bills_table)

#         # Create assets table
#         create_assets_table = """
#         CREATE TABLE assets (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_on DATE,
#             disposed_type VARCHAR(50),
#             disposed_reason VARCHAR(255),
#             sold_to VARCHAR(255),
#             sold_price DECIMAL(10,2),
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_assets_table)

#         # Create asset_images table
#         create_asset_images_table = """
#         CREATE TABLE asset_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_images_table)

#         # Create asset_bills table
#         create_asset_bills_table = """
#         CREATE TABLE asset_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_bills_table)

#         # Create asset_history table
#         create_asset_history_table = """
#         CREATE TABLE asset_history (
#             history_id INT AUTO_INCREMENT PRIMARY KEY,
#             table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department)',
#             entity_id INT NOT NULL COMMENT 'ID of the entity (asset_id, component_id, device_id, user_id, category_id, department_id)',
#             data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
#             action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
#             action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
#         );
#         """
#         cursor.execute(create_asset_history_table)

#         # Create job_cards table with updated fields
#         create_job_cards_table = """
#         CREATE TABLE job_cards (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             job_number VARCHAR(20) NOT NULL UNIQUE,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             status ENUM('Open', 'Started', 'Completed') DEFAULT 'Open',
#             created_date DATE,
#             started_date DATE,
#             completed_date DATE,
#             department_id INT NOT NULL,
#             asset_id INT,
#             closure_details TEXT,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_job_cards_table)

#         # Commit changes
#         connection.commit()
#         print("Database tables recreated successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

# # Call the function to recreate the database tables
# recreate_database()



# import mysql.connector

# def recreate_database():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Drop existing tables individually (adjusted order to handle foreign key constraints)
#         drop_statements = [
#             "DROP TABLE IF EXISTS asset_history;",
#             "DROP TABLE IF EXISTS asset_bills;",
#             "DROP TABLE IF EXISTS asset_images;",
#             "DROP TABLE IF EXISTS job_cards;",
#             "DROP TABLE IF EXISTS consumable_images;",
#             "DROP TABLE IF EXISTS consumables;",
#             "DROP TABLE IF EXISTS cartridges;",
#             "DROP TABLE IF EXISTS printers;",
#             "DROP TABLE IF EXISTS device_bills;",
#             "DROP TABLE IF EXISTS device_images;",
#             "DROP TABLE IF EXISTS devices;",
#             "DROP TABLE IF EXISTS component_bills;",
#             "DROP TABLE IF EXISTS component_images;",
#             "DROP TABLE IF EXISTS components;",
#             "DROP TABLE IF EXISTS assets;",
#             "DROP TABLE IF EXISTS category;",
#             "DROP TABLE IF EXISTS users;",
#             "DROP TABLE IF EXISTS department;"
#         ]
#         for statement in drop_statements:
#             cursor.execute(statement)

#         # Create department table
#         create_department_table = """
#         CREATE TABLE department (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_department_table)

#         # Create users table
#         create_users_table = """
#         CREATE TABLE users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             emp_id VARCHAR(50) NOT NULL UNIQUE,
#             password VARCHAR(255),
#             branch VARCHAR(100) NOT NULL,
#             department_id INT NOT NULL,
#             can_login TINYINT(1) DEFAULT 0,
#             image_path VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_users_table)

#         # Create category table
#         create_category_table = """
#         CREATE TABLE category (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             type VARCHAR(50) NOT NULL,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_category_table)

#         # Create assets table
#         create_assets_table = """
#         CREATE TABLE assets (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_on DATE,
#             disposed_type VARCHAR(50),
#             disposed_reason VARCHAR(255),
#             sold_to VARCHAR(255),
#             sold_price DECIMAL(10,2),
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_assets_table)

#         # Create components table
#         create_components_table = """
#         CREATE TABLE components (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             category_id INT,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_asset VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_components_table)

#         # Create devices table
#         create_devices_table = """
#         CREATE TABLE devices (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             distributor_name VARCHAR(255),
#             distributor_location VARCHAR(255),
#             device_tag VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_devices_table)

#         # Create printers table
#         create_printers_table = """
#         CREATE TABLE printers (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             cartridge_no VARCHAR(255),
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_printers_table)

#         # Create consumables table
#         create_consumables_table = """
#         CREATE TABLE consumables (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             available_quantity INT NOT NULL DEFAULT 0,
#             status ENUM('Available', 'Deployed', 'Consumed') DEFAULT 'Available',
#             deployed_to INT,
#             deployed_on DATE,
#             consumed_by VARCHAR(255),
#             consumption_date DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_to) REFERENCES assets(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_consumables_table)

#         # Create cartridges table
#         create_cartridges_table = """
#         CREATE TABLE cartridges (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cartridge_no VARCHAR(255) NOT NULL,
#             printer_model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_cartridges_table)

#         # Create component_images table
#         create_component_images_table = """
#         CREATE TABLE component_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_images_table)

#         # Create component_bills table
#         create_component_bills_table = """
#         CREATE TABLE component_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_bills_table)

#         # Create device_images table
#         create_device_images_table = """
#         CREATE TABLE device_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_images_table)

#         # Create device_bills table
#         create_device_bills_table = """
#         CREATE TABLE device_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_bills_table)

#         # Create asset_images table
#         create_asset_images_table = """
#         CREATE TABLE asset_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_images_table)

#         # Create asset_bills table
#         create_asset_bills_table = """
#         CREATE TABLE asset_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_bills_table)

#         # Create consumable_images table
#         create_consumable_images_table = """
#         CREATE TABLE consumable_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_images_table)

#         # Create asset_history table
#         create_asset_history_table = """
#         CREATE TABLE asset_history (
#             history_id INT AUTO_INCREMENT PRIMARY KEY,
#             table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department)',
#             entity_id INT NOT NULL COMMENT 'ID of the entity (asset_id, component_id, device_id, user_id, category_id, department_id)',
#             data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
#             action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
#             action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
#         );
#         """
#         cursor.execute(create_asset_history_table)

#         # Create job_cards table with updated fields
#         create_job_cards_table = """
#         CREATE TABLE job_cards (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             job_number VARCHAR(20) NOT NULL UNIQUE,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             status ENUM('Open', 'Started', 'Completed') DEFAULT 'Open',
#             created_date DATE,
#             started_date DATE,
#             completed_date DATE,
#             department_id INT NOT NULL,
#             asset_id INT,
#             closure_details TEXT,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_job_cards_table)

#         # Commit changes
#         connection.commit()
#         print("Database tables recreated successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

# # Call the function to recreate the database tables
# recreate_database()


# import mysql.connector

# def recreate_database():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Drop existing tables individually (adjusted order to handle foreign key constraints)
#         drop_statements = [
#             "DROP TABLE IF EXISTS asset_history;",
#             "DROP TABLE IF EXISTS asset_bills;",
#             "DROP TABLE IF EXISTS asset_images;",
#             "DROP TABLE IF EXISTS job_cards;",
#             "DROP TABLE IF EXISTS consumable_bills;",
#             "DROP TABLE IF EXISTS consumable_images;",
#             "DROP TABLE IF EXISTS consumables;",
#             "DROP TABLE IF EXISTS cartridges;",
#             "DROP TABLE IF EXISTS printers;",
#             "DROP TABLE IF EXISTS device_bills;",
#             "DROP TABLE IF EXISTS device_images;",
#             "DROP TABLE IF EXISTS devices;",
#             "DROP TABLE IF EXISTS component_bills;",
#             "DROP TABLE IF EXISTS component_images;",
#             "DROP TABLE IF EXISTS components;",
#             "DROP TABLE IF EXISTS assets;",
#             "DROP TABLE IF EXISTS category;",
#             "DROP TABLE IF EXISTS users;",
#             "DROP TABLE IF EXISTS department;"
#         ]
#         for statement in drop_statements:
#             cursor.execute(statement)

#         # Create department table
#         create_department_table = """
#         CREATE TABLE department (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_department_table)

#         # Create users table
#         create_users_table = """
#         CREATE TABLE users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             emp_id VARCHAR(50) NOT NULL UNIQUE,
#             password VARCHAR(255),
#             branch VARCHAR(100) NOT NULL,
#             department_id INT NOT NULL,
#             can_login TINYINT(1) DEFAULT 0,
#             image_path VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_users_table)

#         # Create category table
#         create_category_table = """
#         CREATE TABLE category (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             type VARCHAR(50) NOT NULL,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_category_table)

#         # Create assets table
#         create_assets_table = """
#         CREATE TABLE assets (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_on DATE,
#             disposed_type VARCHAR(50),
#             disposed_reason VARCHAR(255),
#             sold_to VARCHAR(255),
#             sold_price DECIMAL(10,2),
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_assets_table)

#         # Create components table
#         create_components_table = """
#         CREATE TABLE components (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             category_id INT,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_asset VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             deployed_on DATE,  -- Added
#             disposed_on DATE,  -- Added
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_components_table)

#         # Create devices table
#         create_devices_table = """
#         CREATE TABLE devices (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) DEFAULT 'Available' NOT NULL,
#             distributor_name VARCHAR(255),
#             distributor_location VARCHAR(255),
#             device_tag VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_devices_table)

#         # Create printers table
#         create_printers_table = """
#         CREATE TABLE printers (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             cartridge_no VARCHAR(255),
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             location VARCHAR(255) NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Fixed syntax
#         );
#         """
#         cursor.execute(create_printers_table)

#         # Create cartridges table
#         create_cartridges_table = """
#         CREATE TABLE cartridges (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cartridge_no VARCHAR(255) NOT NULL,
#             printer_model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_cartridges_table)

#         # Create consumables table with cartridge_id
#         create_consumables_table = """
#         CREATE TABLE consumables (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,  -- Should match cartridges.printer_model
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             available_quantity INT NOT NULL DEFAULT 0,
#             status ENUM('Available', 'Deployed', 'Consumed') DEFAULT 'Available',
#             cartridge_id INT,
#             deployed_to INT,  -- Now references printers.id
#             deployed_on DATE,
#             consumed_by VARCHAR(255),
#             consumption_date DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (cartridge_id) REFERENCES cartridges(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_to) REFERENCES printers(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_consumables_table)

#         # Create component_images table
#         create_component_images_table = """
#         CREATE TABLE component_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_images_table)

#         # Create component_bills table
#         create_component_bills_table = """
#         CREATE TABLE component_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_bills_table)

#         # Create device_images table
#         create_device_images_table = """
#         CREATE TABLE device_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_images_table)

#         # Create device_bills table
#         create_device_bills_table = """
#         CREATE TABLE device_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_bills_table)

#         # Create asset_images table
#         create_asset_images_table = """
#         CREATE TABLE asset_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_images_table)

#         # Create asset_bills table
#         create_asset_bills_table = """
#         CREATE TABLE asset_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_bills_table)

#         # Create consumable_images table
#         create_consumable_images_table = """
#         CREATE TABLE consumable_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_images_table)

#         # Create consumable_bills table
#         create_consumable_bills_table = """
#         CREATE TABLE consumable_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_bills_table)

#         # Create asset_history table
#         create_asset_history_table = """
#         CREATE TABLE asset_history (
#             history_id INT AUTO_INCREMENT PRIMARY KEY,
#             table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department)',
#             entity_id INT NOT NULL COMMENT 'ID of the entity (asset_id, component_id, device_id, user_id, category_id, department_id)',
#             data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
#             action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
#             action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
#         );
#         """
#         cursor.execute(create_asset_history_table)

#         # Create job_cards table with updated fields
#         create_job_cards_table = """
#         CREATE TABLE job_cards (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             job_number VARCHAR(20) NOT NULL UNIQUE,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             status ENUM('Open', 'Started', 'Completed') DEFAULT 'Open',
#             created_date DATE,
#             started_date DATE,
#             completed_date DATE,
#             department_id INT NOT NULL,
#             asset_id INT,
#             closure_details TEXT,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_job_cards_table)

#         # Commit changes
#         connection.commit()
#         print("Database tables recreated successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

# # Call the function to recreate the database tables
# recreate_database()



# import mysql.connector

# def recreate_database():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Drop existing tables in order to handle foreign key constraints
#         drop_statements = [
#             "DROP TABLE IF EXISTS asset_history;",
#             "DROP TABLE IF EXISTS asset_bills;",
#             "DROP TABLE IF EXISTS asset_images;",
#             "DROP TABLE IF EXISTS job_cards;",
#             "DROP TABLE IF EXISTS consumable_bills;",
#             "DROP TABLE IF EXISTS consumable_images;",
#             "DROP TABLE IF EXISTS consumables;",
#             "DROP TABLE IF EXISTS cartridges;",
#             "DROP TABLE IF EXISTS printers;",
#             "DROP TABLE IF EXISTS device_bills;",
#             "DROP TABLE IF EXISTS device_images;",
#             "DROP TABLE IF EXISTS devices;",
#             "DROP TABLE IF EXISTS component_bills;",
#             "DROP TABLE IF EXISTS component_images;",
#             "DROP TABLE IF EXISTS components;",
#             "DROP TABLE IF EXISTS assets;",
#             "DROP TABLE IF EXISTS category;",
#             "DROP TABLE IF EXISTS users;",
#             "DROP TABLE IF EXISTS department;"
#         ]
#         for statement in drop_statements:
#             cursor.execute(statement)

#         # Create department table
#         create_department_table = """
#         CREATE TABLE department (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_department_table)

#         # Create users table
#         create_users_table = """
#         CREATE TABLE users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             emp_id VARCHAR(50) NOT NULL UNIQUE,
#             password VARCHAR(255),
#             branch VARCHAR(100) NOT NULL,
#             department_id INT NOT NULL,
#             can_login TINYINT(1) DEFAULT 0,
#             image_path VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_users_table)

#         # Create category table
#         create_category_table = """
#         CREATE TABLE category (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             type VARCHAR(50) NOT NULL,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_category_table)

#         # Create assets table
#         create_assets_table = """
#         CREATE TABLE assets (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_on DATE,
#             disposed_type VARCHAR(50),
#             disposed_reason VARCHAR(255),
#             sold_to VARCHAR(255),
#             sold_price DECIMAL(10,2),
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_assets_table)

#         # Create components table
#         create_components_table = """
#         CREATE TABLE components (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             category_id INT,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_asset VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             deployed_on DATE,
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_components_table)

#         # Create devices table
#         create_devices_table = """
#         CREATE TABLE devices (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             distributor_name VARCHAR(255),
#             distributor_location VARCHAR(255),
#             device_tag VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_devices_table)

#         # Create printers table without purchase_date
#         create_printers_table = """
#         CREATE TABLE printers (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         model VARCHAR(255) NOT NULL,
#         company VARCHAR(255) NOT NULL,
#         cartridge_no VARCHAR(255),
#         location VARCHAR(255) NOT NULL,
#         department_id INT,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#         FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_printers_table)

#         # Create cartridges table
#         create_cartridges_table = """
#         CREATE TABLE cartridges (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cartridge_no VARCHAR(255) NOT NULL UNIQUE,
#             printer_model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_cartridges_table)

#         # Create consumables table
#         create_consumables_table = """
#         CREATE TABLE consumables (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         cartridge_no VARCHAR(255) NOT NULL,
#         company VARCHAR(255) NOT NULL,
#         location VARCHAR(255) NOT NULL,
#         purchase_date DATE NOT NULL,
#         available_quantity INT NOT NULL DEFAULT 0,
#         status ENUM('Available', 'Deployed', 'Consumed') NOT NULL DEFAULT 'Available',
#         cartridge_id INT,
#         deployed_to INT,
#         deployed_on DATE,
#         consumed_by VARCHAR(255),
#         description TEXT,
#         consumption_date DATE,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#         FOREIGN KEY (cartridge_id) REFERENCES cartridges(id) ON DELETE SET NULL,
#         FOREIGN KEY (deployed_to) REFERENCES printers(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_consumables_table)

#         # Create component_images table
#         create_component_images_table = """
#         CREATE TABLE component_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_images_table)

#         # Create component_bills table
#         create_component_bills_table = """
#         CREATE TABLE component_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_bills_table)

#         # Create device_images table
#         create_device_images_table = """
#         CREATE TABLE device_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_images_table)

#         # Create device_bills table
#         create_device_bills_table = """
#         CREATE TABLE device_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_bills_table)

#         # Create asset_images table
#         create_asset_images_table = """
#         CREATE TABLE asset_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_images_table)

#         # Create asset_bills table
#         create_asset_bills_table = """
#         CREATE TABLE asset_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_bills_table)

#         # Create consumable_images table
#         create_consumable_images_table = """
#         CREATE TABLE consumable_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_images_table)

#         # Create consumable_bills table
#         create_consumable_bills_table = """
#         CREATE TABLE consumable_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_bills_table)

#         # Create asset_history table
#         create_asset_history_table = """
#         CREATE TABLE asset_history (
#             history_id INT AUTO_INCREMENT PRIMARY KEY,
#             table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department, printers, consumables)',
#             entity_id INT NOT NULL COMMENT 'ID of the entity',
#             data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
#             action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
#             action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
#         );
#         """
#         cursor.execute(create_asset_history_table)

#         # Create job_cards table
#         create_job_cards_table = """
#         CREATE TABLE job_cards (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             job_number VARCHAR(20) NOT NULL UNIQUE,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             status ENUM('Open', 'Started', 'Completed') NOT NULL DEFAULT 'Open',
#             created_date DATE,
#             started_date DATE,
#             completed_date DATE,
#             department_id INT NOT NULL,
#             asset_id INT,
#             closure_details TEXT,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_job_cards_table)

#         # Commit changes
#         connection.commit()
#         print("Database tables recreated successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'connection' in locals():
#             connection.close()

# if __name__ == "__main__":
#     recreate_database()




# import mysql.connector

# def recreate_database():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Drop existing tables in order to handle foreign key constraints
#         drop_statements = [
#             "DROP TABLE IF EXISTS asset_history;",
#             "DROP TABLE IF EXISTS asset_bills;",
#             "DROP TABLE IF EXISTS asset_images;",
#             "DROP TABLE IF EXISTS job_cards;",
#             "DROP TABLE IF EXISTS consumable_bills;",
#             "DROP TABLE IF EXISTS consumable_images;",
#             "DROP TABLE IF EXISTS consumables;",
#             "DROP TABLE IF EXISTS cartridges;",
#             "DROP TABLE IF EXISTS printers;",
#             "DROP TABLE IF EXISTS device_bills;",
#             "DROP TABLE IF EXISTS device_images;",
#             "DROP TABLE IF EXISTS devices;",
#             "DROP TABLE IF EXISTS component_bills;",
#             "DROP TABLE IF EXISTS component_images;",
#             "DROP TABLE IF EXISTS components;",
#             "DROP TABLE IF EXISTS assets;",
#             "DROP TABLE IF EXISTS category;",
#             "DROP TABLE IF EXISTS users;",
#             "DROP TABLE IF EXISTS department;"
#         ]
#         for statement in drop_statements:
#             cursor.execute(statement)

#         # Create department table
#         create_department_table = """
#         CREATE TABLE department (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_department_table)

#         # Create users table
#         create_users_table = """
#         CREATE TABLE users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             emp_id VARCHAR(50) NOT NULL UNIQUE,
#             password VARCHAR(255),
#             branch VARCHAR(100) NOT NULL,
#             department_id INT NOT NULL,
#             can_login TINYINT(1) DEFAULT 0,
#             image_path VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_users_table)

#         # Create category table
#         create_category_table = """
#         CREATE TABLE category (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             type VARCHAR(50) NOT NULL,
#             description TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_category_table)

#         # Create assets table
#         create_assets_table = """
#         CREATE TABLE assets (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_on DATE,
#             disposed_type VARCHAR(50),
#             disposed_reason VARCHAR(255),
#             sold_to VARCHAR(255),
#             sold_price DECIMAL(10,2),
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_assets_table)

#         # Create components table
#         create_components_table = """
#         CREATE TABLE components (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             category_id INT,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             deployed_type VARCHAR(50),
#             deployed_user_id INT,
#             deployed_department_id INT,
#             deployed_asset VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             deployed_on DATE,
#             disposed_on DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_components_table)

#         # Create devices table
#         create_devices_table = """
#         CREATE TABLE devices (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             serial_number VARCHAR(255) NOT NULL UNIQUE,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             status VARCHAR(50) NOT NULL DEFAULT 'Available',
#             distributor_name VARCHAR(255),
#             distributor_location VARCHAR(255),
#             device_tag VARCHAR(255),
#             disposed_reason VARCHAR(255),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_devices_table)

#         # Create printers table
#         create_printers_table = """
#         CREATE TABLE printers (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             cartridge_no VARCHAR(255),
#             location VARCHAR(255) NOT NULL,
#             department_id INT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_printers_table)

#         # Create cartridges table
#         create_cartridges_table = """
#         CREATE TABLE cartridges (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cartridge_no VARCHAR(255) NOT NULL UNIQUE,
#             printer_model VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         );
#         """
#         cursor.execute(create_cartridges_table)

#         # Create consumables table
#         create_consumables_table = """
#         CREATE TABLE consumables (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cartridge_no VARCHAR(255) NOT NULL,
#             company VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             purchase_date DATE NOT NULL,
#             available_quantity INT NOT NULL DEFAULT 0,
#             status ENUM('Available', 'Deployed', 'Consumed') NOT NULL DEFAULT 'Available',
#             cartridge_id INT,
#             deployed_to INT,
#             deployed_on DATE,
#             consumed_by VARCHAR(255),
#             description TEXT,
#             consumption_date DATE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#             FOREIGN KEY (cartridge_id) REFERENCES cartridges(id) ON DELETE SET NULL,
#             FOREIGN KEY (deployed_to) REFERENCES printers(id) ON DELETE SET NULL
#         );
#         """
#         cursor.execute(create_consumables_table)

#         # Create component_images table
#         create_component_images_table = """
#         CREATE TABLE component_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_images_table)

#         # Create component_bills table
#         create_component_bills_table = """
#         CREATE TABLE component_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             component_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_component_bills_table)

#         # Create device_images table
#         create_device_images_table = """
#         CREATE TABLE device_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_images_table)

#         # Create device_bills table
#         create_device_bills_table = """
#         CREATE TABLE device_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             device_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_device_bills_table)

#         # Create asset_images table
#         create_asset_images_table = """
#         CREATE TABLE asset_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_images_table)

#         # Create asset_bills table
#         create_asset_bills_table = """
#         CREATE TABLE asset_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             asset_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_asset_bills_table)

#         # Create consumable_images table
#         create_consumable_images_table = """
#         CREATE TABLE consumable_images (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             image_name VARCHAR(255) NOT NULL,
#             image_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_images_table)

#         # Create consumable_bills table
#         create_consumable_bills_table = """
#         CREATE TABLE consumable_bills (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             consumable_id INT NOT NULL,
#             bill_name VARCHAR(255) NOT NULL,
#             bill_data LONGBLOB NOT NULL,
#             FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
#         );
#         """
#         cursor.execute(create_consumable_bills_table)

#         # Create asset_history table
#         create_asset_history_table = """
#         CREATE TABLE asset_history (
#             history_id INT AUTO_INCREMENT PRIMARY KEY,
#             table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department, printers, consumables)',
#             entity_id INT NOT NULL COMMENT 'ID of the entity',
#             data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
#             action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
#             action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
#         );
#         """
#         cursor.execute(create_asset_history_table)

#         # Create job_cards table
#         create_job_cards_table = """
#         CREATE TABLE job_cards (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             job_number VARCHAR(20) NOT NULL UNIQUE,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             status ENUM('Open', 'Started', 'Completed') NOT NULL DEFAULT 'Open',
#             created_date DATE,
#             started_date DATE,
#             completed_date DATE,
#             department_id INT NOT NULL,
#             entity_type ENUM('Asset', 'Consumable', 'Component', 'Device'),
#             entity_id INT,
#             closure_details TEXT,
#             FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
#         );
#         """
#         cursor.execute(create_job_cards_table)

#         # Commit changes
#         connection.commit()
#         print("Database tables recreated successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'connection' in locals():
#             connection.close()

# if __name__ == "__main__":
#     recreate_database()




import mysql.connector

def recreate_database():
    try:
        # Connect to MySQL server and use the asm_sys database
        connection = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="asm_sys"
        )
        cursor = connection.cursor()

        # Drop existing tables in order to handle foreign key constraints
        drop_statements = [
            "DROP TABLE IF EXISTS asset_history;",
            "DROP TABLE IF EXISTS asset_bills;",
            "DROP TABLE IF EXISTS asset_images;",
            "DROP TABLE IF EXISTS job_cards;",
            "DROP TABLE IF EXISTS consumable_bills;",
            "DROP TABLE IF EXISTS consumable_images;",
            "DROP TABLE IF EXISTS consumables;",
            "DROP TABLE IF EXISTS cartridges;",
            "DROP TABLE IF EXISTS printers;",
            "DROP TABLE IF EXISTS device_bills;",
            "DROP TABLE IF EXISTS device_images;",
            "DROP TABLE IF EXISTS devices;",
            "DROP TABLE IF EXISTS component_bills;",
            "DROP TABLE IF EXISTS component_images;",
            "DROP TABLE IF EXISTS components;",
            "DROP TABLE IF EXISTS assets;",
            "DROP TABLE IF EXISTS category;",
            # "DROP TABLE IF EXISTS users;",
            # "DROP TABLE IF EXISTS department;"
        ]
        for statement in drop_statements:
            cursor.execute(statement)

        # Create department table
        create_department_table = """
        CREATE TABLE department (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_department_table)

        # Create users table
        create_users_table = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            emp_id VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255),
            branch VARCHAR(100) NOT NULL,
            department_id INT NOT NULL,
            can_login TINYINT(1) DEFAULT 0,
            image_path VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
        );
        """
        cursor.execute(create_users_table)

        # Create category table
        create_category_table = """
        CREATE TABLE category (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            type VARCHAR(50) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_category_table)

        # Create assets table
        create_assets_table = """
        CREATE TABLE assets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model VARCHAR(255) NOT NULL,
            serial_number VARCHAR(255) NOT NULL UNIQUE,
            company VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            purchase_date DATE NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Available',
            deployed_type VARCHAR(50),
            deployed_user_id INT,
            deployed_department_id INT,
            deployed_on DATE,
            disposed_type VARCHAR(50),
            disposed_reason VARCHAR(255),
            sold_to VARCHAR(255),
            sold_price DECIMAL(10,2),
            disposed_on DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
        );
        """
        cursor.execute(create_assets_table)

        # Create components table
        create_components_table = """
        CREATE TABLE components (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            model VARCHAR(255) NOT NULL,
            serial_number VARCHAR(255) NOT NULL UNIQUE,
            company VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            purchase_date DATE NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Available',
            deployed_type VARCHAR(50),
            deployed_user_id INT,
            deployed_department_id INT,
            deployed_asset VARCHAR(255),
            disposed_reason VARCHAR(255),
            deployed_on DATE,
            disposed_on DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
            FOREIGN KEY (deployed_user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (deployed_department_id) REFERENCES department(id) ON DELETE SET NULL
        );
        """
        cursor.execute(create_components_table)

        # Create devices table
        create_devices_table = """
        CREATE TABLE devices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model VARCHAR(255) NOT NULL,
            serial_number VARCHAR(255) NOT NULL UNIQUE,
            company VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            purchase_date DATE NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Available',
            distributor_name VARCHAR(255),
            distributor_location VARCHAR(255),
            device_tag VARCHAR(255),
            disposed_reason VARCHAR(255),
            deployed_on DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_devices_table)

        # Create printers table
        create_printers_table = """
        CREATE TABLE printers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model VARCHAR(255) NOT NULL,
            company VARCHAR(255) NOT NULL,
            cartridge_no VARCHAR(255),
            location VARCHAR(255) NOT NULL,
            department_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE SET NULL
        );
        """
        cursor.execute(create_printers_table)

        # Create cartridges table
        create_cartridges_table = """
        CREATE TABLE cartridges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cartridge_no VARCHAR(255) NOT NULL UNIQUE,
            printer_model VARCHAR(255) NOT NULL,
            company VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_cartridges_table)

        # Create consumables table
        create_consumables_table = """
        CREATE TABLE consumables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cartridge_no VARCHAR(255) NOT NULL,
            company VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            purchase_date DATE NOT NULL,
            available_quantity INT NOT NULL DEFAULT 0,
            status ENUM('Available', 'Deployed', 'Consumed') NOT NULL DEFAULT 'Available',
            cartridge_id INT,
            deployed_to INT,
            deployed_on DATE,
            consumed_by VARCHAR(255),
            description TEXT,
            consumption_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (cartridge_id) REFERENCES cartridges(id) ON DELETE SET NULL,
            FOREIGN KEY (deployed_to) REFERENCES printers(id) ON DELETE SET NULL
        );
        """
        cursor.execute(create_consumables_table)

        # Create component_images table
        create_component_images_table = """
        CREATE TABLE component_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            component_id INT NOT NULL,
            image_name VARCHAR(255) NOT NULL,
            image_data LONGBLOB NOT NULL,
            FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_component_images_table)

        # Create component_bills table
        create_component_bills_table = """
        CREATE TABLE component_bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            component_id INT NOT NULL,
            bill_name VARCHAR(255) NOT NULL,
            bill_data LONGBLOB NOT NULL,
            FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_component_bills_table)

        # Create device_images table
        create_device_images_table = """
        CREATE TABLE device_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id INT NOT NULL,
            image_name VARCHAR(255) NOT NULL,
            image_data LONGBLOB NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_device_images_table)

        # Create device_bills table
        create_device_bills_table = """
        CREATE TABLE device_bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id INT NOT NULL,
            bill_name VARCHAR(255) NOT NULL,
            bill_data LONGBLOB NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_device_bills_table)

        # Create asset_images table
        create_asset_images_table = """
        CREATE TABLE asset_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            asset_id INT NOT NULL,
            image_name VARCHAR(255) NOT NULL,
            image_data LONGBLOB NOT NULL,
            last_sync DATETIME
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_asset_images_table)

        # Create asset_bills table
        create_asset_bills_table = """
        CREATE TABLE asset_bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            asset_id INT NOT NULL,
            bill_name VARCHAR(255) NOT NULL,
            bill_data LONGBLOB NOT NULL,
            last_sync DATETIME
            FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_asset_bills_table)

        # Create consumable_images table
        create_consumable_images_table = """
        CREATE TABLE consumable_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            consumable_id INT NOT NULL,
            image_name VARCHAR(255) NOT NULL,
            image_data LONGBLOB NOT NULL,
            FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_consumable_images_table)

        # Create consumable_bills table
        create_consumable_bills_table = """
        CREATE TABLE consumable_bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            consumable_id INT NOT NULL,
            bill_name VARCHAR(255) NOT NULL,
            bill_data LONGBLOB NOT NULL,
            FOREIGN KEY (consumable_id) REFERENCES consumables(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_consumable_bills_table)

        # Create asset_history table
        create_asset_history_table = """
        CREATE TABLE asset_history (
            history_id INT AUTO_INCREMENT PRIMARY KEY,
            table_type VARCHAR(50) NOT NULL COMMENT 'Type of entity (e.g., assets, components, devices, users, category, department, printers, consumables)',
            entity_id INT NOT NULL COMMENT 'ID of the entity',
            data_json JSON NOT NULL COMMENT 'JSON representation of the entity state',
            action VARCHAR(50) NOT NULL COMMENT 'Action type: Added, Updated, Deleted',
            action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the action occurred'
        );
        """
        cursor.execute(create_asset_history_table)

        # Create job_cards table
        create_job_cards_table = """
            CREATE TABLE job_cards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_number VARCHAR(20) NOT NULL UNIQUE,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status ENUM('Open', 'Started', 'Completed') NOT NULL DEFAULT 'Open',
                created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                started_date DATETIME,
                completed_date DATETIME,
                department_id INT NOT NULL,
                entity_type ENUM('Asset', 'Consumable', 'Component', 'Device'),
                entity_id INT,
                closure_details TEXT,
                FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE RESTRICT
            );
            """
        cursor.execute(create_job_cards_table)

        # Commit changes
        connection.commit()
        print("Database tables recreated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    recreate_database()