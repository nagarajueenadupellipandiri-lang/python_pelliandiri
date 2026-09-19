from sqlalchemy import Column, Integer, String
from database import Base

class EnRaasiMaster(Base):
    __tablename__ = "en_raasi_master"

    raasi_id = Column( Integer, primary_key=True, autoincrement=True )
    raasi = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    