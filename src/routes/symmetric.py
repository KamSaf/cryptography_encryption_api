from fastapi import APIRouter, Depends, HTTPException
import os
from sqlalchemy.orm import Session
from src.db_stuff.utils import get_db
from src.db_stuff.models import SymmetricKey
from src.models.models import NewSymmetricKey, Message
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from src.db_stuff.utils import get_sym_key as get_key

router = APIRouter()

KEY_LENGTH = 64
IV_LENGTH = 16


@router.get("/symmetric/key")
def get_sym_key():
    """
    Return randomly generated symmetric key.
    """
    return {"Randomly generated symmetric key": os.urandom(32).hex()}


@router.post("/symmetric/key")
def post_sym_key(post_data: NewSymmetricKey | None = None, db: Session = Depends(get_db)):
    """
    Sets symmetric key on the server
    """
    if not post_data or not post_data.key:
        raise HTTPException(status_code=400, detail="No key provided")
    # if len(post_data.key) != KEY_LENGTH or type(post_data.key) is not str:
    #     raise HTTPException(status_code=411, detail="Key must be 64 characters long string")
    try:
        key_obj = SymmetricKey(key=post_data.key)
        db.add(key_obj)
        db.commit()
        return {"message": "New symmetric key succesfully set"}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/symmetric/encode")
def post_sym_encode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Endpoint returning encrypted form of given message, using currently set symmetric key.
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No message provided")
    try:
        key = bytes.fromhex(get_key(db))
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_msg = bytes(post_data.message, 'utf-8').ljust(16, b"\0")
        encr_msg = (encryptor.update(padded_msg) + encryptor.finalize()).hex()
        return {"Encrypted message": encr_msg + iv.hex()}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/symmetric/decode")
def post_sym_decode(post_data: Message | None = None, db: Session = Depends(get_db)):
    """
    Endpoint returning decrypted form of given message, using currently set symmetric key.
    """
    if not post_data or not post_data.message:
        raise HTTPException(status_code=400, detail="No key provided")
    try:
        key = bytes.fromhex(get_key(db))
        iv = bytes.fromhex(post_data.message[32:])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decr_msg = decryptor.update(bytes.fromhex(post_data.message[:32])) + decryptor.finalize()
        return {"Decrypted message": decr_msg.rstrip(b"\0")}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")
