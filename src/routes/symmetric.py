from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session
from src.db_stuff.utils import get_db
from src.db_stuff.models import SymmetricKey
from src.models.models import SetSymmetricKey

router = APIRouter()


@router.get("/symmetric/key")
def get_sym_key():
    """
    Return randomly generated symmetric key.
    """
    return {"Randomly generated symmetric key": os.urandom(32).hex()}


@router.post("/symmetric/key")
def post_sym_key(post_data: SetSymmetricKey, db: Session = Depends(get_db)):
    """
    ustawia na serwerze klucz symetryczny podany w postaci HEX w request
    """
    if len(post_data.key) != 64:
        return {"message": "Key must be 64 characters long"}

    try:
        key_obj = SymmetricKey()
        db.add(key_obj)
        db.commit()
        return {"message": "New symmetric key succesfully set"}
    except Exception as e:
        return {"error": e}


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