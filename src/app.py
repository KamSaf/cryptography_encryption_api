from fastapi import FastAPI, Depends
import os
from sqlalchemy.orm import Session
from utils import get_db
from config import engine, Base
from db_models import SymmetricKey
from models import SetSymmetricKey

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/symmetric/key")
def get_sym_key():
    """
    Return randomly generated symmetric key.
    """
    return {"Randomly generated symmetric key": os.urandom(32).hex()}


@app.post("/symmetric/key")
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


@app.post("/symmetric/encode")
def post_sym_encode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
    """
    return {"message": "Hello World"}


@app.post("/symmetric/decode")
def post_sym_decode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
    """
    return {"message": "Hello World"}

# ASYMMETRIC #


@app.get("/asymmetric/key")
def get_asym_key():
    """
    zwraca nowy klucz publiczny i prywatny w postaci HEX (w JSON jako dict) i ustawia go na serwerze
    """
    return {"message": "Hello World"}


@app.get("/asymmetric/key/ssh")
def get_key_ssh():
    """
    zwraca klucz publiczny i prywatny w postaci HEX zapisany w formacie OpenSSH
    """
    return {"message": "Hello World"}


@app.post("/asymmetric/key")
def post_asym_key():
    """
    ustawia na serwerze klucz publiczny i prywatny w postaci HEX (w JSON jako dict)
    """
    return {"message": "Hello World"}


@app.post("/asymmetric/verify")
def post_asym_verify():
    """
    korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
    """
    return {"message": "Hello World"}


@app.post("/asymmetric/sign")
def post_asym_sign():
    """
    korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
    """
    return {"message": "Hello World"}


@app.post("/asymmetric/encode")
def post_asym_encode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
    """
    return {"message": "Hello World"}


@app.post("/asymmetric/decode")
def post_asym_decode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
    """
    return {"message": "Hello World"}