from src.db_stuff.config import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sym_key(db: Session):
    return "aa800b403438f72208d8846787c15aa8640d8dac3e0f41ac9021da6bc2bae4f6"


if __name__ == "__main__":
    pass
