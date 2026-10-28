from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database import Base

class EnPackageCategories(Base):
    __tablename__ = "en_package_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(50), nullable=True)
    datecreated = Column( TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP") )
    status = Column(Integer, nullable=True)
