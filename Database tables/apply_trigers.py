# import mysql.connector

# def apply_triggers():
#     try:
#         # Connect to MySQL server and use the asm_sys database
#         connection = mysql.connector.connect(
#             host="200.200.200.23",
#             user="root",
#             password="Pak@123",
#             database="asm_sys"
#         )
#         cursor = connection.cursor()

#         # Trigger for Assets Insert
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_asset_insert
#         AFTER INSERT ON assets
#         FOR EACH ROW
#         BEGIN
#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'assets', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NEW.deployed_type, NEW.deployed_user_id, NEW.deployed_department_id, NEW.deployed_on,
#                 NEW.disposed_type, NEW.disposed_reason, NEW.sold_to, NEW.sold_price, NEW.disposed_on,
#                 NEW.created_at, NEW.updated_at, 'Added'
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Trigger for Assets Update
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_asset_update
#         AFTER UPDATE ON assets
#         FOR EACH ROW
#         BEGIN
#             DECLARE action_type VARCHAR(50);

#             IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
#                 SET action_type = 'Deployed';
#             ELSEIF NEW.status IN ('Dispose', 'Sold') AND OLD.status NOT IN ('Dispose', 'Sold') THEN
#                 IF NEW.status = 'Dispose' THEN
#                     SET action_type = 'Disposed';
#                 ELSE
#                     SET action_type = 'Sold';
#                 END IF;
#             ELSE
#                 SET action_type = 'Updated';
#             END IF;

#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'assets', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NEW.deployed_type, NEW.deployed_user_id, NEW.deployed_department_id, NEW.deployed_on,
#                 NEW.disposed_type, NEW.disposed_reason, NEW.sold_to, NEW.sold_price, NEW.disposed_on,
#                 NEW.created_at, NEW.updated_at, action_type
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Trigger for Components Insert
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_component_insert
#         AFTER INSERT ON components
#         FOR EACH ROW
#         BEGIN
#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'components', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NEW.deployed_type, NEW.deployed_user_id, NEW.deployed_department_id, NULL,
#                 NULL, NEW.disposed_reason, NULL, NULL, NULL,
#                 NEW.created_at, NEW.updated_at, 'Added'
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Trigger for Components Update
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_component_update
#         AFTER UPDATE ON components
#         FOR EACH ROW
#         BEGIN
#             DECLARE action_type VARCHAR(50);

#             IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
#                 SET action_type = 'Deployed';
#             ELSEIF NEW.status IN ('Dispose') AND OLD.status NOT IN ('Dispose') THEN
#                 SET action_type = 'Disposed';
#             ELSE
#                 SET action_type = 'Updated';
#             END IF;

#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'components', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NEW.deployed_type, NEW.deployed_user_id, NEW.deployed_department_id, NULL,
#                 NULL, NEW.disposed_reason, NULL, NULL, NULL,
#                 NEW.created_at, NEW.updated_at, action_type
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Trigger for Devices Insert
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_device_insert
#         AFTER INSERT ON devices
#         FOR EACH ROW
#         BEGIN
#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'devices', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NULL, NULL, NULL, NULL,
#                 NULL, NEW.disposed_reason, NULL, NULL, NULL,
#                 NEW.created_at, NEW.updated_at, 'Added'
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Trigger for Devices Update
#         cursor.execute("""
#         DELIMITER //

#         CREATE TRIGGER after_device_update
#         AFTER UPDATE ON devices
#         FOR EACH ROW
#         BEGIN
#             DECLARE action_type VARCHAR(50);

#             IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
#                 SET action_type = 'Deployed';
#             ELSEIF NEW.status IN ('Dispose') AND OLD.status NOT IN ('Dispose') THEN
#                 SET action_type = 'Disposed';
#             ELSE
#                 SET action_type = 'Updated';
#             END IF;

#             INSERT INTO asset_history (
#                 table_type, entity_id, model, serial_number, company, location, purchase_date,
#                 status, deployed_type, deployed_user_id, deployed_department_id, deployed_on,
#                 disposed_type, disposed_reason, sold_to, sold_price, disposed_on,
#                 created_at, updated_at, action
#             )
#             VALUES (
#                 'devices', NEW.id, NEW.model, NEW.serial_number, NEW.company, NEW.location, NEW.purchase_date,
#                 NEW.status, NULL, NULL, NULL, NULL,
#                 NULL, NEW.disposed_reason, NULL, NULL, NULL,
#                 NEW.created_at, NEW.updated_at, action_type
#             );
#         END //

#         DELIMITER ;
#         """)

#         # Commit changes
#         connection.commit()
#         print("Triggers applied successfully.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

# # Call the function to apply triggers
# apply_triggers()


import mysql.connector
import json

def apply_triggers():
    try:
        # Connect to MySQL server and use the asm_sys database
        connection = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="asm_sys"
        )
        cursor = connection.cursor()

        # Trigger for Assets Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_asset_insert
        AFTER INSERT ON assets
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('assets', NEW.id, JSON_OBJECT(
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'deployed_type', NEW.deployed_type,
                'deployed_user_id', NEW.deployed_user_id,
                'deployed_department_id', NEW.deployed_department_id,
                'deployed_on', NEW.deployed_on,
                'disposed_type', NEW.disposed_type,
                'disposed_reason', NEW.disposed_reason,
                'sold_to', NEW.sold_to,
                'sold_price', NEW.sold_price,
                'disposed_on', NEW.disposed_on,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Assets Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_asset_update
        AFTER UPDATE ON assets
        FOR EACH ROW
        BEGIN
            DECLARE action_type VARCHAR(50);
            IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
                SET action_type = 'Deployed';
            ELSEIF NEW.status IN ('Dispose', 'Sold') AND OLD.status NOT IN ('Dispose', 'Sold') THEN
                IF NEW.status = 'Dispose' THEN
                    SET action_type = 'Disposed';
                ELSE
                    SET action_type = 'Sold';
                END IF;
            ELSE
                SET action_type = 'Updated';
            END IF;

            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('assets', NEW.id, JSON_OBJECT(
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'deployed_type', NEW.deployed_type,
                'deployed_user_id', NEW.deployed_user_id,
                'deployed_department_id', NEW.deployed_department_id,
                'deployed_on', NEW.deployed_on,
                'disposed_type', NEW.disposed_type,
                'disposed_reason', NEW.disposed_reason,
                'sold_to', NEW.sold_to,
                'sold_price', NEW.sold_price,
                'disposed_on', NEW.disposed_on,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), action_type);
        END //

        DELIMITER ;
        """)

        # Trigger for Components Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_component_insert
        AFTER INSERT ON components
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('components', NEW.id, JSON_OBJECT(
                'category_id', NEW.category_id,
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'deployed_type', NEW.deployed_type,
                'deployed_user_id', NEW.deployed_user_id,
                'deployed_department_id', NEW.deployed_department_id,
                'deployed_asset', NEW.deployed_asset,
                'disposed_reason', NEW.disposed_reason,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Components Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_component_update
        AFTER UPDATE ON components
        FOR EACH ROW
        BEGIN
            DECLARE action_type VARCHAR(50);
            IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
                SET action_type = 'Deployed';
            ELSEIF NEW.status IN ('Dispose') AND OLD.status NOT IN ('Dispose') THEN
                SET action_type = 'Disposed';
            ELSE
                SET action_type = 'Updated';
            END IF;

            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('components', NEW.id, JSON_OBJECT(
                'category_id', NEW.category_id,
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'deployed_type', NEW.deployed_type,
                'deployed_user_id', NEW.deployed_user_id,
                'deployed_department_id', NEW.deployed_department_id,
                'deployed_asset', NEW.deployed_asset,
                'disposed_reason', NEW.disposed_reason,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), action_type);
        END //

        DELIMITER ;
        """)

        # Trigger for Devices Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_device_insert
        AFTER INSERT ON devices
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('devices', NEW.id, JSON_OBJECT(
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'distributor_name', NEW.distributor_name,
                'distributor_location', NEW.distributor_location,
                'device_tag', NEW.device_tag,
                'disposed_reason', NEW.disposed_reason,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Devices Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_device_update
        AFTER UPDATE ON devices
        FOR EACH ROW
        BEGIN
            DECLARE action_type VARCHAR(50);
            IF NEW.status = 'Deployed' AND OLD.status != 'Deployed' THEN
                SET action_type = 'Deployed';
            ELSEIF NEW.status IN ('Dispose') AND OLD.status NOT IN ('Dispose') THEN
                SET action_type = 'Disposed';
            ELSE
                SET action_type = 'Updated';
            END IF;

            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('devices', NEW.id, JSON_OBJECT(
                'model', NEW.model,
                'serial_number', NEW.serial_number,
                'company', NEW.company,
                'location', NEW.location,
                'purchase_date', NEW.purchase_date,
                'status', NEW.status,
                'distributor_name', NEW.distributor_name,
                'distributor_location', NEW.distributor_location,
                'device_tag', NEW.device_tag,
                'disposed_reason', NEW.disposed_reason,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), action_type);
        END //

        DELIMITER ;
        """)

        # Trigger for Users Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_users_insert
        AFTER INSERT ON users
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('users', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'emp_id', NEW.emp_id,
                'password', NEW.password,
                'branch', NEW.branch,
                'department_id', NEW.department_id,
                'can_login', NEW.can_login,
                'image_path', NEW.image_path,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Users Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_users_update
        AFTER UPDATE ON users
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('users', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'emp_id', NEW.emp_id,
                'password', NEW.password,
                'branch', NEW.branch,
                'department_id', NEW.department_id,
                'can_login', NEW.can_login,
                'image_path', NEW.image_path,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Updated');
        END //

        DELIMITER ;
        """)

        # Trigger for Category Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_category_insert
        AFTER INSERT ON category
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('category', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'type', NEW.type,
                'description', NEW.description,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Category Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_category_update
        AFTER UPDATE ON category
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('category', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'type', NEW.type,
                'description', NEW.description,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Updated');
        END //

        DELIMITER ;
        """)

        # Trigger for Department Insert
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_department_insert
        AFTER INSERT ON department
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('department', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'description', NEW.description,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Added');
        END //

        DELIMITER ;
        """)

        # Trigger for Department Update
        cursor.execute("""
        DELIMITER //

        CREATE TRIGGER after_department_update
        AFTER UPDATE ON department
        FOR EACH ROW
        BEGIN
            INSERT INTO asset_history (table_type, entity_id, data_json, action)
            VALUES ('department', NEW.id, JSON_OBJECT(
                'name', NEW.name,
                'description', NEW.description,
                'created_at', NEW.created_at,
                'updated_at', NEW.updated_at
            ), 'Updated');
        END //

        DELIMITER ;
        """)

        # Commit changes
        connection.commit()
        print("Triggers applied successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Call the function to apply triggers
apply_triggers()