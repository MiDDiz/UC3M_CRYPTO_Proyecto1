from cryptography.hazmat.primitives import hashes


def passwordHash(passw:str)->bytes:
    passwb = str.encode(passw)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(passwb)
    dec_passw=digest.finalize()
    dec_passw = str(dec_passw)
    return dec_passw
