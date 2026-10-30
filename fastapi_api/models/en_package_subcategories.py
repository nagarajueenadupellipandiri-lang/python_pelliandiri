from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database import Base


class EnPackageSubcategories(Base):
    __tablename__ = "en_package_subcategories"

    cid = Column(Integer, primary_key=True, autoincrement=True)
    main_catid = Column(Integer, nullable=False)
    subcatname = Column(String(50), nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    status = Column(Integer, nullable=True)