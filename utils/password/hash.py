
import hashlib

# def encrypt_password(password: str) -> str:
#     # Generate salt and hash
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed.decode('utf-8')

# def verify_password(stored_hash: str, password: str) -> bool:
#     return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def encrypt_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash: str, password: str) -> bool:
    return encrypt_password(password) == stored_hash