from database import create_connection

connection = create_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Buildings")

    buildings = cursor.fetchall()

    print("\nList of Buildings:")

    for building in buildings:
        print(building)

    cursor.close()
    connection.close()