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

        # Drop job_cards table if it exists
        drop_job_cards_table = "DROP TABLE IF EXISTS job_cards;"
        cursor.execute(drop_job_cards_table)

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

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    recreate_database()