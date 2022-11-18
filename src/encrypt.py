from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, generate_private_key, RSAPublicKey
from os import urandom


def password_hash(passw: str) -> str:
    passwb = str.encode(passw)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(passwb)
    dec_passw = digest.finalize()
    dec_passw = str(dec_passw)
    return dec_passw


def generate_salt() -> str:
    newsalt = urandom(32)
    newsalt = str(newsalt)
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


def get_private_key() -> RSAPrivateKey:
    """
    :return: Returns a newly generated private key
    """
    return generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )


def get_public_key(private_key: RSAPrivateKey) -> RSAPublicKey:
    """
    Re-encapsulation of the method below.
    :param private_key: The private key from the public key
    :return: Returns the public key from the private key
    """
    private_key.public_key()


def sign_message(message: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Retruns the signature of the un-hashed message
    :param message:
    :param private_key:
    :return:
    """
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


def verify_signature(signature: bytes, message: bytes, public_key: RSAPublicKey) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Signature is valid
        return True
    except InvalidSignature:
        # Simply put the signature is invalid
        return False
    except Exception as e:
        # Unexpected error
        raise ValueError("Fatal error handling verification signature") from e
