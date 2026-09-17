from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    address = Column(Text, nullable=False)
    dob = Column(String(15), nullable=False)
    contact_no = Column(String(16), nullable=False)

    verification_code = Column(String(255), nullable=False)

    created_date = Column(String(12), nullable=False)
    modified_date = Column(String(12), nullable=False)

    status = Column(String(1), nullable=False)