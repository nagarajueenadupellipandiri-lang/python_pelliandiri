from sqlalchemy import Column, Integer, String, Text, Enum
from database import Base


class EnBanners(Base):
    __tablename__ = "en_banners"

    id = Column(Integer, primary_key=True, autoincrement=True)

    banner_type = Column( Enum("before_login", "after_login"), nullable=False, default="before_login" )

    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    image = Column(String(100), nullable=False)
    alttext = Column(String(255), nullable=True)
    caption = Column(String(255), nullable=True)

    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    status = Column(Integer, nullable=True, default=1)
    deleted = Column(Integer, nullable=True, default=0)
