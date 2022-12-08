from argon2 import PasswordHasher


def generate_hash(raw_password):
    password_hasher = PasswordHasher()
    return password_hasher.hash(raw_password)
