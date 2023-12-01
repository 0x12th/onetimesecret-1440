import base64
import uuid

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.config import settings


def generate_secret_key() -> str:
    return uuid.uuid4().hex


def get_hash(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def check_hash(password: str, known_hash: str) -> bool:
    ph = PasswordHasher()
    return ph.verify(known_hash, password)


def encrypt(secret_message: str, passphrase: str) -> str:
    salt = settings.SALT.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    f = Fernet(key)

    encrypted_message = f.encrypt(secret_message.encode("utf-8"))

    return encrypted_message.decode("utf-8")


def decrypt(encrypted_message: str, passphrase: str) -> str:
    salt = settings.SALT.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    f = Fernet(key)

    decrypted_message = f.decrypt(encrypted_message.encode("utf-8"))

    return decrypted_message.decode("utf-8")
