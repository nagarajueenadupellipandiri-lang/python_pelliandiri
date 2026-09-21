from sqlalchemy import Column, Integer, String
from database import Base

class EnOccupationMasterHead(Base):
    __tablename__ = "en_occupation_master_head"

    cat_id = Column( Integer, primary_key=True, autoincrement=True )
    cat_name = Column(String(50), nullable=True)
    