import random
import string

def generate_password(length=12, include_numbers=False, include_special_chars=False):
    """
    Generate a random password with customizable options.

    Args:
        length (int, optional): Length of the generated password (default is 12).
        include_numbers (bool, optional): Include numbers in the password (default is False).
        include_special_chars (bool, optional): Include special characters in the password (default is False).

    Returns:
        str: A randomly generated password.
    """
    characters = string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password
