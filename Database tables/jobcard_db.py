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

        # Create job_cards table
        create_job_cards_table = """
        CREATE TABLE IF NOT EXISTS job_cards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status ENUM('Open', 'Closed') DEFAULT 'Open',
            asset_id INT,
            FOREIGN KEY (asset_id) REFERENCES assets(id)
        );
        """
        cursor.execute(create_job_cards_table)

        # Commit changes
        connection.commit()
        print("job_cards table created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Call the function to create the table
recreate_database()