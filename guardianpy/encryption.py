from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import hashlib

master_password = None  # Initialize the master password as None

def generate_key(master_password, user_id):
    # Hash the user_id to create a 32-byte salt
    salt = (hashlib.sha256(user_id.to_bytes(32, 'big'))).digest()

    # Generate an encryption key using PBKDF2HMAC with the hashed user_id as salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


def encrypt_password(password, key):
    # Encrypt a password using Fernet
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    # Decrypt an encrypted password using Fernet
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def set_master_password(password):
    # Set the global master password
    global master_password
    master_password = password

def get_master_password():
    # Retrieve the master password
    return master_password
