import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, generate_private_key, RSAPublicKey
from os import urandom


def password_hash(passw: str) -> str:
	"""
	Return a string representation of the hash of passw.
	We use this method to hash passwords.
	"""
    passwb = str.encode(passw)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(passwb)
    dec_passw = digest.finalize()
    dec_passw = str(dec_passw)
    return dec_passw


def generate_salt() -> str:
	"""
	Generate and stringify a salt
	"""
    newsalt = urandom(32)
    newsalt = str(newsalt)
    return newsalt


def generate_secret_datakey(passwd: str, salt: str) -> bytes:
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
    return private_key.public_key()


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
	"""
	Checks whether the signature was made with the message and the private key that public_key represents.
	"""
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
        # Unexpected error -> We catch everything and re-raise it 
        raise ValueError("Fatal error handling verification signature") from e


def text_to_bytes(text: str) -> bytes:
    """
    Returns a reday to use base-64 encoded stream of bytes representing the text given
    :param text: Text to convert
    :return: Base64'd of the text converted
    """
    return base64.b64encode(text.encode("utf-8"))


def b64text_to_bytes(b64text: str) -> bytes:
    """
    Returns a ready to use bytestream from a base64 encoded stream dumped into a string
    :param b64text: string containing the base64 text representation of the desired stream
    :return: the desired stream
    """
    return base64.decodebytes(b64text.encode("utf-8"))


def bytes_to_text(stream: bytes):
    """
    Returns the string representation of a base-64 encoded stream
    :param stream: The data desired to encode and dump into string
    :return: The string representing the data in base-64
    """
    return base64.b64encode(stream).decode("utf-8")

def text_to_b64text(text: str):
	"""
	Sometimes we need to store JSON sensive text so we parse it to safe Base64 and store it that way.
	Also it serves as obfuscation
	"""
	return text_to_bytes(text).decode("utf-8")

def b64text_to_text(text: str):
	"""
	When we have b64text stored in a JSON file we would like to have the text de-encoded
	This method returns the plaintext message encoded on text from a base64 encoding.
	"""
	return b64text_to_bytes(text).decode("utf-8")

def serialized_public_key(ku: RSAPublicKey) -> bytes:
	"""
	Encapsulation for getting the serialized public key from our RSAPublicKey object
	"""
    return ku.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def deserialize_public_key(serialized_public_key: str) -> RSAPublicKey:
	"""
	Encapsulation for getting the RSAPublicKey object from the stored serialized public key
	"""
    return serialization.load_pem_public_key(
        serialized_public_key.encode("utf-8")
    )


def serialize_private_key(private_key: RSAPrivateKey, passwd: bytes) -> bytes:
	"""
	Encapsulation for getting the serialized private key from our RSAPrivateKey object while encrypting it with the password
	"""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passwd)
    )


def deserialize_private_key(serialized_private_key: str, passwd: bytes) -> RSAPrivateKey:
	"""
	De-encription and deserialization of the private key stored. We use the password to decript it.
	"""
    print(f"Obtenemos: \n{serialized_private_key}\n\n\n\n")
    #print(text_to_bytes(serialized_private_key).decode("utf-8"))
    return serialization.load_pem_private_key(
        serialized_private_key.encode("utf-8"),
        password=passwd
    )
