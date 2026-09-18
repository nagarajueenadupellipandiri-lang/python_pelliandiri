from sqlalchemy import Column, Integer, String
from database import Base

class EnHeightMaster(Base):
    __tablename__ = "en_height_master"

    height_id = Column( Integer, primary_key=True, autoincrement=True )
    height = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    