import secrets
import string

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits  # only letters & numbers
    return ''.join(secrets.choice(characters) for _ in range(length))
