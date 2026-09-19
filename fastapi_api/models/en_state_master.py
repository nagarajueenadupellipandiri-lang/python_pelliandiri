from sqlalchemy import Column, Integer, String
from database import Base

class EnStateMaster(Base):
    __tablename__ = "en_state_master"

    state_id = Column( Integer, primary_key=True, autoincrement=True )
    state_name = Column(String(100), nullable=True)
    country_id_old = Column(Integer, nullable=True)
    country_id = Column(Integer, nullable=True)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)