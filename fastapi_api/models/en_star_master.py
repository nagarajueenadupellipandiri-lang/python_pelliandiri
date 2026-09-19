from sqlalchemy import Column, Integer, String
from database import Base

class EnStarMaster(Base):
    __tablename__ = "en_star_master"

    star_id = Column( Integer, primary_key=True, autoincrement=True )
    star = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    