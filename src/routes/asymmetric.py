from cryptography.hazmat.primitives import hashes
from fastapi import APIRouter, Depends, HTTPException
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption
from src.db_stuff.models import AsymmetricKeys
from src.db_stuff.utils import get_db
from sqlalchemy.orm import Session
from src.models.models import NewAsymmetricKeys, Message


router = APIRouter()

ENCRYPTION_PASSWORD = b"MEGAWONSZ9"


@router.get("/asymmetric/key")
def get_asym_key(db: Session = Depends(get_db)) -> dict:
    """
    Returns new private and public asymmetric keys and sets them on the server.
    """
    try:
        private_key_obj = rsa.generate_private_key(public_exponent=65537, key_size=2048)
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

        key_obj = AsymmetricKeys(private_key=private_key_hex, public_key=public_key_hex)
        db.add(key_obj)
        db.commit()

        return {
            "public key": public_key_hex,
            "private key": private_key_hex,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.get("/asymmetric/key/ssh")
def get_key_ssh() -> dict:
    """
    Returns new private and public asymmetric keys in an OpenSSH format.
    """
    try:
        private_key_obj = rsa.generate_private_key(public_exponent=65537, key_size=2048)
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

        return {
            "public key ssh": public_key_hex,
            "private key ssh": private_key_hex,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/asymmetric/key")
def post_asym_key(post_data: NewAsymmetricKeys | None = None, db: Session = Depends(get_db)) -> dict:
    """
    Sets private and public asymmetric keys on the server.
    """
    if not post_data:
        raise HTTPException(status_code=400, detail="No keys provided")
    if not post_data.private_key:
        raise HTTPException(status_code=400, detail="No private key provided")
    if not post_data.public_key:
        raise HTTPException(status_code=400, detail="No public key provided")

    try:
        key_obj = AsymmetricKeys(private_key=post_data.private_key, public_key=post_data.public_key)
        db.add(key_obj)
        db.commit()
        return {"message": "New symmetric key succesfully set"}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/asymmetric/verify")
def post_asym_verify():
    """
    korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/sign")
def post_asym_sign():
    """
    korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/encode")
def post_asym_encode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
    """
    # MESSAGE = "hello this is a message"
    # encr = public_key_obj.encrypt(plaintext=MESSAGE.encode(), padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    # decr = private_key_obj.decrypt(ciphertext=encr, padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return {"message": "Hello World"}


@router.post("/asymmetric/decode")
def post_asym_decode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    pass
