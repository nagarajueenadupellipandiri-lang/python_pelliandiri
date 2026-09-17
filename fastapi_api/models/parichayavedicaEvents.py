from sqlalchemy import Column, Integer, String, Text
from database import Base


class parichayavedicaEvents(Base):
    __tablename__ = "en_parichaya_vedika"

    id = Column(Integer, primary_key=True, autoincrement=True)

    eng_title = Column(String(100), nullable=False)
    caste_id = Column(Integer, nullable=False)

    address = Column(Text, nullable=False)
    venue_address = Column(String(16), nullable=False)

    online_link = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)

    start_date = Column(String(12), nullable=False)
    end_date = Column(String(12), nullable=False)
    display_date = Column(String(12), nullable=False)
    display_time = Column(String(12), nullable=False)

    status = Column(String(1), nullable=False)