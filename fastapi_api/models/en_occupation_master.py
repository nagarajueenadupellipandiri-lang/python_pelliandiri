from sqlalchemy import Column, Integer, String
from database import Base

class EnOccupationMaster(Base):
    __tablename__ = "en_occupation_master"

    occupation_id = Column( Integer, primary_key=True, autoincrement=True )
    occupation = Column(String(50), nullable=True)
    occupation_category = Column(Integer, nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    