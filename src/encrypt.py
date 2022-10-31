from cryptography.hazmat.primitives import hashes
from os import urandom


def password_hash(passw: str) -> str:
    passwb = str.encode(passw)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(passwb)
    dec_passw = digest.finalize()
    dec_passw = str(dec_passw)
    return dec_passw


def generate_salt() -> str:
    newsalt= urandom(32)
    newsalt=str(newsalt)
    return newsalt


def generate_secret_datakey(passwd: str, salt: bytes) -> bytes:
    """
    Generate HASH-256 from data in order to use it to encrypt-decrypt AES256 information.
    :param passwd: usr plaintext passwd
    :param salt: salt used for this iteration of encryption
    :return: secret key (HASH256)
    """
    # Generate new hash digest
    digest = hashes.Hash(hashes.SHA256())
    # update digest with
    digest.update(str.encode(passwd))
    digest.update(str.encode(salt))
    return digest.finalize()


