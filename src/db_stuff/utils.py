from src.db_stuff.config import SessionLocal
from sqlalchemy.orm import Session
from src.db_stuff.models import SymmetricKey
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


if __name__ == "__main__":
    pass
