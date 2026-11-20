
import mysql.connector
import hashlib
import secrets
import getpass

from database import create_connection


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        600000
    ).hex()

    return f"{salt}${password_hash}"


connection = create_connection()

if connection:
    cursor = connection.cursor()

    accounts = [
    ("System Admin", "admin")
    ]

    for name, login_id in accounts:
        print(f"\nSet password for {name} ({login_id})")

        password = getpass.getpass("Enter password: ")
        confirm = getpass.getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match. Please run the program again.")
            break

        if len(password) < 8:
            print("Password must have at least 8 characters.")
            break

        hashed = hash_password(password)

        cursor.execute(
            "UPDATE Users SET password_hash = %s WHERE login_id = %s",
            (hashed, login_id)
        )

        connection.commit()
        print(f"Password successfully saved for {name}!")

    cursor.close()
    connection.close()
