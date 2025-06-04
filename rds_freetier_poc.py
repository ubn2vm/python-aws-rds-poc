import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Database Connection Details ---
# The following variables are loaded from the .env file
# or set as environment variables in the shell.
DB_HOST = os.environ.get('DB_HOST_POC')
DB_USER = os.environ.get('DB_USER_POC')
DB_PASSWORD = os.environ.get('DB_PASSWORD_POC')
DB_NAME = os.environ.get('DB_NAME_POC')

def recreate_tech_consultants_table(connection, cursor):
    """
    Drops the 'tech_consultants' table if it exists, and then recreates it.
    This ensures a clean table for each execution.
    """
    try:
        # Drop the table if it already exists
        drop_table_query = "DROP TABLE IF EXISTS tech_consultants;"
        cursor.execute(drop_table_query)
        print(f"Table 'tech_consultants' dropped if it existed in database '{DB_NAME}'.")

        # Create the table
        create_table_query = """
        CREATE TABLE tech_consultants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            specialty VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        print(f"Table 'tech_consultants' created in database '{DB_NAME}'.")
    except Error as e:
        print(f"Error recreating table 'tech_consultants': {e}")
        raise # Re-raise the exception to stop execution if table recreation fails

def insert_consultant_data(connection, cursor, name, specialty):
    """Inserts new consultant data into the tech_consultants table."""
    try:
        sql = "INSERT INTO tech_consultants (name, specialty) VALUES (%s, %s)"
        val = (name, specialty)
        cursor.execute(sql, val)
        connection.commit() # Commit the transaction to save changes
        print(f"Inserted: Name={name}, Specialty={specialty}. Rows affected: {cursor.rowcount}")
    except Error as e:
        print(f"Error inserting data: {e}")

def retrieve_consultant_data(cursor):
    """Reads all data from the tech_consultants table and prints it."""
    try:
        cursor.execute("SELECT id, name, specialty FROM tech_consultants")
        records = cursor.fetchall()
        print("\n--- Tech Consultants Data ---")
        if records:
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Specialty: {row[2]}")
        else:
            print("No records found (as expected after table recreation).") # Updated message
        print("-----------------------------")
    except Error as e:
        print(f"Error reading data: {e}")

def main():
    connection = None # Initialize connection to None for finally block
    # Check if all required environment variables are set
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        print("Error: DB_HOST_POC, DB_USER_POC, DB_PASSWORD_POC, and DB_NAME_POC environment variables must be set.")
        print("Example for Linux/macOS: export DB_HOST_POC='your-rds-instance.region.rds.amazonaws.com'")
        print("Example for Windows: set DB_HOST_POC=your-rds-instance.region.rds.amazonaws.com")
        return # Exit if a variable is missing

    try:
        # Connect to the specified MySQL database on RDS
        # This will fail if DB_NAME does not exist on the server
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME # Connect directly to the specified database
        )

        if connection.is_connected():
            print(f"Successfully connected to RDS MySQL database: {DB_NAME}!")
            cursor = connection.cursor()

            # Recreate the 'tech_consultants' table (drops if exists, then creates)
            recreate_tech_consultants_table(connection, cursor) # Updated function call

            print("\n--- Performing End-to-End Operations ---")
            # 1. Insert some sample data
            print("Inserting new data...")
            insert_consultant_data(connection, cursor, "Carol Danvers", "Python & RDS Free Tier")
            insert_consultant_data(connection, cursor, "Peter Parker", "Data Analysis")
            insert_consultant_data(connection, cursor, "Tony Stark", "Advanced Engineering")


            # 2. Read the data from the table
            retrieve_consultant_data(cursor)

            # You can also add UPDATE or DELETE operations here to demonstrate full CRUD functionality.

            cursor.close() # Close the cursor

    except Error as e:
        print(f"Error connecting to or working with MySQL Database: {e}")
    finally:
        # Ensure the database connection is closed even if an error occurs
        if connection and connection.is_connected():
            connection.close()
            print("\nMySQL connection is closed.")

if __name__ == "__main__":
    # This ensures main() is called only when the script is executed directly
    main()