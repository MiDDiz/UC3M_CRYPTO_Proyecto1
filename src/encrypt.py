from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
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


def encrypt_data(data_key: bytes, data: bytes) -> tuple[bytes, bytes]:
    """
    # USING AES256 -> Block size: 16 bytes
    This method gets a secret key and some data to be encrypted.
    :param data_key: Is the secret key to be used to encrypt data.
    :param data: Data to be encrypted.
    :return:    init_vector: We need to return init_vector in order to be able to decrypt the data after.
                encrypted_message: The bytes of the encrypteed message.
    """

    # Generate input vector for cipher CBC mode.
    init_vector = urandom(16)
    cipher = Cipher(algorithms.AES256(data_key), modes.CTR(init_vector))
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(data) + encryptor.finalize()
    return init_vector, encrypted_message


def decrypt_data(data_key: bytes, init_vector: bytes, message: bytes):
    """
    Decrypts the message with the data_key and the init_vector for CBC
    :param data_key: the secret data_key
    :param init_vector: the init_vector for CBC
    :param message: the message to be decrypted
    :return: the decrypted message
    """
    cipher = Cipher(algorithms.AES(data_key), modes.CTR(init_vector))
    decryptor = cipher.decryptor()
    return decryptor.update(message) + decryptor.finalize()
