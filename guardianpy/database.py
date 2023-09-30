import sqlite3
import hashlib
import os

def initialize_database():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    # Create a table to store user accounts and passwords
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        salt BLOB,
                        password BLOB
                     )''')

    # Create a table to store website-specific passwords
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        website TEXT,
                        password TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                     )''')

    conn.commit()
    conn.close()

    
def register_user(username, password):
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    try:
        # Generate a random salt
        salt = os.urandom(32)  # 32 bytes for the salt
        password_bytes = password.encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)

        cursor.execute("INSERT INTO users (username, salt, password) VALUES (?, ?, ?)", (username, salt, password_hash))

        conn.commit()
        conn.close()

        print("Registration Successful.")
    except Exception as e:
        print("Registration Failed:", e)
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, salt, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            stored_salt = user[1]
            stored_password_hash = user[2]

            password_bytes = password.encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, stored_salt, 100000)

            # Compare the password_hash with the stored_password_hash
            if password_hash == stored_password_hash:
                return user[0]

        print("Authentication Failed: Invalid username or password.")
    except Exception as e:
        print("Authentication Failed:", e)
    finally:
        conn.close()

    return None




def store_password(user_id, website, password):
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)", (user_id, website, password))

    conn.commit()
    conn.close()

def retrieve_password(user_id, website):
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM passwords WHERE user_id=? AND website=?", (user_id, website))
    password = cursor.fetchone()

    if password:
        return password[0]

    return None
