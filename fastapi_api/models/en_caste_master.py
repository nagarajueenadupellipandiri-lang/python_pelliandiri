from sqlalchemy import Column, Integer, String
from database import Base

class EnCasteMaster(Base):
    __tablename__ = "en_caste_master"

    caste_id = Column( Integer, primary_key=True, autoincrement=True )
    caste_name = Column(String(100), nullable=True)
    religion_id = Column(Integer, nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)