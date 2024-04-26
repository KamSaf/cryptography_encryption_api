from src.db_stuff.config import SessionLocal
from sqlalchemy.orm import Session
from src.db_stuff.models import SymmetricKey, AsymmetricKeys
from sqlalchemy import select
from fastapi import HTTPException


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sym_key(db: Session) -> str:
    stmt = select(SymmetricKey.key).order_by(SymmetricKey.create_date.desc())
    result = db.execute(stmt).first()
    key = result[0] if result else None
    if not key:
        raise HTTPException(status_code=422, detail="No symmetric key set on the server")
    return key


def get_asym_keys(db: Session) -> dict:
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
