from sqlalchemy import Column, Integer, String
from database import Base

class EnCity(Base):
    __tablename__ = "en_city"

    city_id = Column( Integer, primary_key=True, autoincrement=True )
    city_name = Column(String(100), nullable=True)
    state_id = Column(Integer, nullable=True)
    country_id = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True, default=1)