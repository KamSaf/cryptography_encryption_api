from sqlalchemy import Column, DateTime, func, Integer, String
from src.db_stuff.config import Base


class SymmetricKey(Base):
    __tablename__ = "symmetric_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    create_date = Column(DateTime(timezone=True), default=func.now())


class AsymmetricKeys(Base):
    __tablename__ = "asymmetric_keys"
    id = Column(Integer, primary_key=True)
    private_key = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    create_date = Column(DateTime(timezone=True), default=func.now())


if __name__ == "__main__":
    pass
