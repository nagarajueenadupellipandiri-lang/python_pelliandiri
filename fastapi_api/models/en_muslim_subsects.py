from sqlalchemy import Column, Integer, String
from database import Base

class EnMuslimSubsects(Base):
    __tablename__ = "en_muslim_subsects"

    denomination_id = Column( Integer, primary_key=True, autoincrement=True )
    denomination = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)