from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def generate_hash(password_raw):
    password_hasher = PasswordHasher()
    return password_hasher.hash(password_raw)


def verify_hash(password_hash, password_raw):
    password_hasher = PasswordHasher()
    verified = False
    message = ""
    try:
        verified = password_hasher.verify(password_hash, password_raw)
    except VerifyMismatchError:
        message = "Invalid password."
    except Exception as err:
        message = f"Unexpected error: \n{err}"

    return verified, message
