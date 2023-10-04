from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64

master_password = None

def generate_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32  
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def set_master_password(password):
    global master_password
    master_password = password

def get_master_password():
    return master_password