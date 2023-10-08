import sqlite3
import hashlib
import os
from guardianpy.encryption import generate_key, encrypt_password, decrypt_password

master_password = None  # Initialize the master password as None

def initialize_database():
    # Initialize the database and create necessary tables if they don't exist
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        salt BLOB,
                        password BLOB
                     )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        website TEXT,
                        email TEXT,
                        password BLOB,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                     )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    # Register a user in the database
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return False
    salt = os.urandom(32)
    password_bytes = password.encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    cursor.execute("INSERT INTO users (username, salt, password) VALUES (?, ?, ?)", (username, salt, password_hash))
    conn.commit()
    conn.close()
    return True

def authenticate_user(username, password):
    # Authenticate a user based on username and password
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, salt, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        stored_salt = user[1]
        stored_password_hash = user[2]
        password_bytes = password.encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, stored_salt, 100000)
        if password_hash == stored_password_hash:
            return user[0]
    conn.close()
    return None

def store_password(user_id, website, email, password, master_password):
    # Store a credential password in the database
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    key = generate_key(master_password, user_id)
    encrypted_password = encrypt_password(password, key)
    cursor.execute("INSERT INTO passwords (user_id, website, email, password) VALUES (?, ?, ?, ?)", (user_id, website, email, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_password(user_id, website, master_password):
    # Retrieve a stored credential password from the database
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM passwords WHERE user_id=? AND website=?", (user_id, website))
    encrypted_password = cursor.fetchone()
    conn.close()
    if encrypted_password:
        key = generate_key(master_password, user_id)
        decrypted_password = decrypt_password(encrypted_password[0], key)
        return decrypted_password
    return None
