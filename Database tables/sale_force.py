import mysql.connector

def insert_sample_data():
    try:
        # Connect to MySQL server and use the asm_sys database
        connection = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="asm_sys"
        )
        cursor = connection.cursor()

        # Insert sample department
        cursor.execute("""
        INSERT INTO department (name, description) VALUES
        ('IT Department', 'Information Technology Department'),
        ('HR Department', 'Human Resources Department');
        """)

        # Insert sample users
        cursor.execute("""
        INSERT INTO users (name, emp_id, password, branch, department_id, can_login) VALUES
        ('John Doe', 'EMP001', 'password123', 'Main Branch', 1, 1),
        ('Jane Smith', 'EMP002', 'password123', 'Main Branch', 2, 1);
        """)

        # Insert sample category
        cursor.execute("""
        INSERT INTO category (name, type, description) VALUES
        ('Laptops', 'Asset', 'Category for laptop assets'),
        ('Monitors', 'Component', 'Category for monitor components');
        """)

        # Commit changes
        connection.commit()
        print("Sample data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Call the function to insert sample data
insert_sample_data()