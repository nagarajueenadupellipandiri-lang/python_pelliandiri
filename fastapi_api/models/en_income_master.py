from sqlalchemy import Column, Integer, String
from database import Base

class EnIncomeMaster(Base):
    __tablename__ = "en_income_master"

    income_id = Column( Integer, primary_key=True, autoincrement=True )
    income = Column(String(50), nullable=False)
    currency_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)
    