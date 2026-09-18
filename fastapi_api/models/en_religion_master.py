from sqlalchemy import Column, Integer, String
from database import Base

class EnReligionMaster(Base):
    __tablename__ = "en_religion_master"

    religion_id = Column( Integer, primary_key=True, autoincrement=True )
    religion_name = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)