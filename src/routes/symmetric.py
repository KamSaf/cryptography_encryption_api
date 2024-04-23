from fastapi import APIRouter, Depends, HTTPException
import os
from sqlalchemy.orm import Session
from src.db_stuff.utils import get_db
from src.db_stuff.models import SymmetricKey
from src.models.models import NewSymmetricKey

router = APIRouter()

KEY_LENGTH = 64


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
    if len(post_data.key) != KEY_LENGTH or type(post_data.key) is not str:
        raise HTTPException(status_code=411, detail="Key must be 64 characters long string")
    try:
        key_obj = SymmetricKey(key=post_data.key)
        db.add(key_obj)
        db.commit()
        return {"message": "New symmetric key succesfully set"}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occured")


@router.post("/symmetric/encode")
def post_sym_encode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
    """
    return {"message": "Hello World"}


@router.post("/symmetric/decode")
def post_sym_decode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
    """
    return {"message": "Hello World"}