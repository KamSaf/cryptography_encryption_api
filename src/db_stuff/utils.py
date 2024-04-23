from src.db_stuff.config import SessionLocal
from sqlalchemy.orm import Session
from src.db_stuff.models import SymmetricKey
from sqlalchemy import select


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sym_key(db: Session) -> str | None:
    stmt = select(SymmetricKey.key).order_by(SymmetricKey.create_date.desc())
    result = db.execute(stmt).first()
    return result[0] if result else None


if __name__ == "__main__":
    pass
