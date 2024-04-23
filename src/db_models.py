from sqlalchemy import Column, DateTime, func, Integer, String
from config import Base


class SymmetricKey(Base):
    __tablename__ = "symmetric_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    create_date = Column(DateTime(timezone=True), default=func.now())
