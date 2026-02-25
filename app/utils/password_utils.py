
#This module provides utilities for password hashing and verification.


# from werkzeug.security import generate_password_hash, check_password_hash


# def hash_password(password: str) -> str:

#     return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(stored_password: str, provided_password: str) -> bool:
    return stored_password == provided_password

