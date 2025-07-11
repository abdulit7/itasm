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

        # Alter asset_images table to add last_sync column
        cursor.execute("ALTER TABLE asset_images ADD COLUMN last_sync DATETIME;")
        print("Column 'last_sync' added to 'asset_images' table.")

        # Alter asset_bills table to add last_sync column
        cursor.execute("ALTER TABLE asset_bills ADD COLUMN last_sync DATETIME;")
        print("Column 'last_sync' added to 'asset_bills' table.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Call the function to alter the tables
recreate_database()