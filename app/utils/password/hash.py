import hashlib

def encrypt_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash: str, password: str) -> bool:
    return encrypt_password(password) == stored_hash