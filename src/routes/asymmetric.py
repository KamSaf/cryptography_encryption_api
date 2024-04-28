from fastapi import APIRouter, Depends, HTTPException
from src.db_stuff.models import AsymmetricKeys
from src.db_stuff.utils import get_db
from sqlalchemy.orm import Session
from src.models.models import NewAsymmetricKeys, Message, MessageToVerify
import src.utils.asymmetric_utils as AU


router = APIRouter()


@router.get("/asymmetric/key")
def get_asym_key(db: Session = Depends(get_db)) -> dict:
    """
    Returns new private and public asymmetric keys and sets them on the server.
    """
    public_key_hex, private_key_hex = AU.generate_rsa_keys()

    try:
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
    public_key_hex, private_key_hex = AU.generate_ssh_rsa_keys()
    try:
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

    Request body:
    --------------------------------------
    private_key -> Private key to be set on the server
    public_key -> Public key to be set on the server
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

    Request body:
    --------------------------------------
    message -> Plain text message
    signature -> Hexadecimal signature
    """
    if not post_data:
        raise HTTPException(status_code=400, detail="No data provided")
    if not post_data.message:
        raise HTTPException(status_code=400, detail="No plain text message provided")
    if not post_data.signature:
        raise HTTPException(status_code=400, detail="No message signature provided")
    result = AU.verify_signature(db=db, message=post_data.message, signature=post_data.signature)
    return {"detail": result}


@router.post("/asymmetric/sign")
def post_asym_sign(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Signs given message with currently set private RSA key.

    Request body:
    --------------------------------------
    message -> Plain text message to be signed
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    signature = AU.sign_message(db=db, message=post_data.message)
    return {"message": post_data.message, "signature": signature}


@router.post("/asymmetric/encode")
def post_asym_encode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Encrypts and returns given message using currently set RSA public key.

    Request body:
    --------------------------------------
    message -> Plain text message to be encrypted
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    return {"encrypted_message": AU.encrypt_message(db=db, message=post_data.message)}


@router.post("/asymmetric/decode")
def post_asym_decode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Decrypts and returns given message using currently set RSA private key.

    Request body:
    --------------------------------------
    message -> Hexadecimal text message to be decrypted
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    return {"decrypted_message": AU.decrypt_message(db=db, message=post_data.message)}


if __name__ == "__main__":
    pass
