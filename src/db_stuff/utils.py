from typing import Iterable
from src.db_stuff.config import SessionLocal
from sqlalchemy.orm import Session
from src.db_stuff.models import SymmetricKey, AsymmetricKeys
from sqlalchemy import select
from fastapi import HTTPException


def get_db() -> Iterable[Session]:
    """
    Function yielding SQLAlchemy database session.

    Yields:
    --------------------------------------
    Iteralbe[Session] -> SQLAlchemy database Session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sym_key(db: Session) -> str:
    """
    Function returning currently set symmetric key from the database.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database Session object

    Returns
    --------------------------------------
    str -> Currently set hexadecimal symmetric key
    """
    stmt = select(SymmetricKey.key).order_by(SymmetricKey.create_date.desc())
    result = db.execute(stmt).first()
    key = result[0] if result else None
    if not key:
        raise HTTPException(status_code=422, detail="No symmetric key set on the server")
    return key


def get_asym_keys(db: Session) -> dict[str, str]:
    """
    Function returning currently set asymmetric private and public keys from the database.

    Parameters:
    --------------------------------------
    db: Session -> SQLAlchemy database Session object

    Returns
    --------------------------------------
    dict[str, str] -> Dictionary containing currently set hexadecimal private and public RSA keys    
    """
    keys = {}
    stmt = select(AsymmetricKeys.private_key, AsymmetricKeys.public_key).order_by(AsymmetricKeys.create_date.desc())
    result = db.execute(stmt).first()
    keys["private_key"] = result[0] if result else None
    keys["public_key"] = result[1] if result else None

    if not keys["private_key"]:
        raise HTTPException(status_code=422, detail="No asymmetric private key set on the server")
    if not keys["public_key"]:
        raise HTTPException(status_code=422, detail="No asymmetric public key set on the server")
    return keys


if __name__ == "__main__":
    pass
