from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, BestAvailableEncryption
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from fastapi import HTTPException
from src.db_stuff.utils import get_asym_keys


ENCRYPTION_PASSWORD = b"MEGAWONSZ9"
PUBLIC_EXPONENT = 65537
KEY_SIZE = 2048


def generate_rsa_keys() -> tuple[str, str]:
    """
    Generates new RSA keys.

    Returns
    --------------------------------------
    tuple[str, str] -> new public and private RSA keys
    """
    private_key_obj = rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=KEY_SIZE)
    public_key_obj = private_key_obj.public_key()
    public_key_hex = public_key_obj.public_bytes(
        encoding=Encoding.DER,
        format=PublicFormat.SubjectPublicKeyInfo
    ).hex()
    private_key_hex = private_key_obj.private_bytes(
        encoding=Encoding.DER,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=BestAvailableEncryption(password=ENCRYPTION_PASSWORD)
    ).hex()
    return public_key_hex, private_key_hex


def generate_ssh_rsa_keys() -> tuple[str, str]:
    """
    Generates new RSA keys in OpenSSH format.

    Returns
    --------------------------------------
    tuple[str, str] -> New public and private RSA keys is OpenSSH format
    """
    private_key_obj = rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=KEY_SIZE)
    public_key_obj = private_key_obj.public_key()
    private_key_hex = private_key_obj.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.OpenSSH,
        encryption_algorithm=BestAvailableEncryption(password=ENCRYPTION_PASSWORD)
    ).hex()
    public_key_hex = public_key_obj.public_bytes(
        encoding=Encoding.OpenSSH,
        format=PublicFormat.OpenSSH
    ).hex()
    return public_key_hex, private_key_hex


def verify_signature(db: Session, message: str, signature: str) -> bool:
    """
    Verifies signature of a given message with current public RSA key.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database session
    message: str -> Plain text message
    signature: str -> Signature of a message to be verified

    Returns:
    --------------------------------------
    bool -> True if signature is valid, False if it is not
    """
    try:
        public_key = get_asym_keys(db=db)["public_key"]
        public_key_obj = serialization.load_der_public_key(data=bytes.fromhex(public_key))
        if isinstance(public_key_obj, rsa.RSAPublicKey):
            public_key_obj.verify(
                signature=bytes.fromhex(signature),
                data=message.encode(),
                padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                algorithm=hashes.SHA256()
            )
        else:
            raise HTTPException(status_code=422, detail="Only RSA ecryption is allowed")
    except InvalidSignature:
        return False
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return True


def sign_message(db: Session, message: str) -> str:
    """
    Returns signature of a given message created with current RSA private key.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database session
    message: str -> Plain text message to be signed

    Returns:
    --------------------------------------
    str -> Hexadecimal signature
    """
    private_key = get_asym_keys(db=db)["private_key"]
    private_key_obj = serialization.load_der_private_key(
        data=bytes.fromhex(private_key),
        password=ENCRYPTION_PASSWORD,
    )
    if isinstance(private_key_obj, rsa.RSAPrivateKey):
        signature = private_key_obj.sign(
            data=message.encode(),
            padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            algorithm=hashes.SHA256()
        )
    else:
        raise HTTPException(status_code=422, detail="Only RSA ecryption is allowed")
    return signature.hex()


def encrypt_message(db: Session, message: str) -> str:
    """
    Encrypts given message with currently set public RSA key.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database session
    message: str -> Plain text message to be encrypted

    Returns:
    --------------------------------------
    str -> Hexadecimal encrypted message
    """
    try:
        public_key = get_asym_keys(db=db)["public_key"]
        public_key_obj = serialization.load_der_public_key(data=bytes.fromhex(public_key))
        if isinstance(public_key_obj, rsa.RSAPublicKey):
            encr = public_key_obj.encrypt(
                plaintext=message.encode(),
                padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
        else:
            raise HTTPException(status_code=422, detail="Only RSA ecryption is allowed")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return encr.hex()


def decrypt_message(db: Session, message: str) -> str:
    """
    Decrypts given message with currently set private RSA key.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database session
    message: str -> Hexadecimal message to be decrypted

    Returns:
    --------------------------------------
    str -> Decrypted message

    """
    try:
        private_key = get_asym_keys(db=db)["private_key"]
        private_key_obj = serialization.load_der_private_key(
            data=bytes.fromhex(private_key),
            password=ENCRYPTION_PASSWORD,
        )
        if isinstance(private_key_obj, rsa.RSAPrivateKey):
            decr = private_key_obj.decrypt(
                ciphertext=bytes.fromhex(message),
                padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
        else:
            raise HTTPException(status_code=422, detail="Only RSA ecryption is allowed")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return decr.decode()


if __name__ == "__main__":
    pass
