from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from fastapi import APIRouter, Depends, HTTPException
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, BestAvailableEncryption
from src.db_stuff.models import AsymmetricKeys
from src.db_stuff.utils import get_db, get_asym_keys
from sqlalchemy.orm import Session
from src.models.models import NewAsymmetricKeys, Message, MessageToVerify

router = APIRouter()

ENCRYPTION_PASSWORD = b"MEGAWONSZ9"


# TODO code refactor, może jakieś sprawdzanie typów? sprawdzanie kluczy zapisywanych przez użytkownika, zaadaptowanie ssh


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
            "public_key": public_key_hex,
            "private_key": private_key_hex,
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
            "public_key_ssh": public_key_hex,
            "private_key_ssh": private_key_hex,
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
def post_asym_verify(post_data: MessageToVerify | None = None, db: Session = Depends(get_db)):
    """
    Verifies signature on given message.
    """
    if not post_data:
        raise HTTPException(status_code=400, detail="No data provided")
    if not post_data.message:
        raise HTTPException(status_code=400, detail="No plain text message provided")
    if not post_data.signature:
        raise HTTPException(status_code=400, detail="No message signature provided")
    try:
        public_key = get_asym_keys(db=db)["public_key"]
        public_key_obj = serialization.load_der_public_key(data=bytes.fromhex(public_key))

        public_key_obj.verify(
            signature=bytes.fromhex(post_data.signature),
            data=post_data.message.encode(),
            padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            algorithm=hashes.SHA256()
        )
    except InvalidSignature:
        return {"detail": False}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return {"detail": True}


@router.post("/asymmetric/sign")
def post_asym_sign(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Signs given message with currently set asymmetric key.
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")

    private_key = get_asym_keys(db=db)["private_key"]
    private_key_obj = serialization.load_der_private_key(
        data=bytes.fromhex(private_key),
        password=ENCRYPTION_PASSWORD,
    )

    signature = private_key_obj.sign(
        data=post_data.message.encode(),
        padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        algorithm=hashes.SHA256()
    )
    return {"message": post_data.message, "signature": signature.hex()}


@router.post("/asymmetric/encode")
def post_asym_encode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Encrypts and returns given message using currently set public key.
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    try:
        public_key = get_asym_keys(db=db)["public_key"]
        public_key_obj = serialization.load_der_public_key(data=bytes.fromhex(public_key))
        encr = public_key_obj.encrypt(
            plaintext=post_data.message.encode(),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return {"encrypted_message": encr.hex()}


@router.post("/asymmetric/decode")
def post_asym_decode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Decrypts and returns given message using currently set private key.
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    try:
        private_key = get_asym_keys(db=db)["private_key"]
        private_key_obj = serialization.load_der_private_key(
            data=bytes.fromhex(private_key),
            password=ENCRYPTION_PASSWORD,
        )
        decr = private_key_obj.decrypt(
            ciphertext=bytes.fromhex(post_data.message),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    return {"decrypted_message": decr}


if __name__ == "__main__":
    pass
