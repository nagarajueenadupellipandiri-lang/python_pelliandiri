from sqlalchemy import Column, Integer, String
from database import Base

class EnCountryMaster(Base):
    __tablename__ = "en_country_master"

    country_id = Column( Integer, primary_key=True, autoincrement=True )
    country_name = Column(String(100), nullable=True)
    isd_code = Column(String(10), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)