from sqlalchemy import Column, Integer, String
from database import Base

class EnQualificationMaster(Base):
    __tablename__ = "en_qualification_master"

    qualification_id = Column( Integer, primary_key=True, autoincrement=True )
    qualification = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    order_id = Column( Integer, nullable=True)
    