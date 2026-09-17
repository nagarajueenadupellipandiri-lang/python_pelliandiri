from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = "en_register"

    register_id = Column(Integer)

    profile_id = Column(String(100))
    password = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    dob = Column(String(255), nullable=False)
    tob = Column(String(255), nullable=False)

    address = Column(Text, nullable=False)
    dob = Column(String(15), nullable=False)
    contact_no = Column(String(16), nullable=False)

    verification_code = Column(String(255), nullable=False)

    created_date = Column(String(12), nullable=False)
    modified_date = Column(String(12), nullable=False)

    status = Column(String(1), nullable=False)