
import os
import mysql.connector


def create_connection():
    """Create a MySQL connection using environment variables."""

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "smart_water_db"),
            port=int(os.getenv("DB_PORT", "3306")),
        )

        if connection.is_connected():
            print("Successfully connected to MySQL!")
            return connection

    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)

    return None


if __name__ == "__main__":
    connection = create_connection()

    if connection:
        connection.close()
        print("Database connection closed.")
