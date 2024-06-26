from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db_stuff.utils import get_db, get_sym_key as get_key
from src.db_stuff.models import SymmetricKey
from src.models.models import NewSymmetricKey, Message
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


router = APIRouter()

IV_LENGTH = 16
HEX_LENGTH = 32
KEY_LENGTH = 64


@router.get("/symmetric/key")
def get_sym_key() -> dict:
    """
    Returns randomly generated symmetric key.
    """
    return {"generated_key": os.urandom(HEX_LENGTH).hex()}


@router.post("/symmetric/key")
def post_sym_key(post_data: NewSymmetricKey | None = None, db: Session = Depends(get_db)) -> dict:
    """
    Sets symmetric key on the server.

    Request body:
    --------------------------------------
    key -> Hexadecimal symmetric key to be set on the server
    """
    if not post_data or not post_data.key:
        raise HTTPException(status_code=400, detail="No key provided")
    if len(post_data.key) != KEY_LENGTH:
        raise HTTPException(status_code=422, detail="Key must be 64 characters long string")
    try:
        key_obj = SymmetricKey(key=post_data.key)
        db.add(key_obj)
        db.commit()
        return {"message": "New symmetric key succesfully set"}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/symmetric/encode")
def post_sym_encode(post_data: Message | None = None, db: Session = Depends(get_db)) -> dict:
    """
    Encrypts given message using currently set symmetric key.

    Request body:
    --------------------------------------
    message -> Plain text message to be encrypted
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    key = get_key(db)
    try:
        hex_key = bytes.fromhex(key)
        iv = os.urandom(IV_LENGTH)
        cipher = Cipher(algorithms.AES(hex_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padding_length = 16 - (len(post_data.message) % 16)
        padded_msg = bytes(post_data.message, 'utf-8').ljust((len(post_data.message) + padding_length), b"\0")
        encr_msg = (encryptor.update(padded_msg) + encryptor.finalize()).hex()
        return {"encrypted_message": encr_msg + iv.hex()}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/symmetric/decode")
def post_sym_decode(post_data: Message | None = None, db: Session = Depends(get_db)) -> dict:
    """
    Decrypts given message using currently set symmetric key.

    Request body:
    --------------------------------------
    message -> Hexadecimal message to be decrypted
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No key provided")
    key = get_key(db)
    try:
        hex_key = bytes.fromhex(key)
        iv = bytes.fromhex(post_data.message[-32:])
        msg = bytes.fromhex(post_data.message[:-32])
        cipher = Cipher(algorithms.AES(hex_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decr_msg = decryptor.update(msg) + decryptor.finalize()
        return {"decrypted_message": decr_msg.rstrip(b"\0")}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


if __name__ == "__main__":
    pass
