from sqlalchemy import Column, Integer, String
from database import Base

class EnChristianDenomination(Base):
    __tablename__ = "en_christian_denomination"

    denomination_id = Column( Integer, primary_key=True, autoincrement=True )
    denomination = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)