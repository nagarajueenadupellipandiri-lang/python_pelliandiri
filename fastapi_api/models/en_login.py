from sqlalchemy import Column, Integer, String, DateTime, Date
from database import Base

class EnLogin(Base):
    __tablename__ = "en_login"

    login_id = Column(Integer, primary_key=True, autoincrement=True)

    emp_id = Column(String(20), nullable=False)
    username = Column(String(100), nullable=False)
    emp_email = Column(String(150), nullable=True)

    password = Column(String(80), nullable=False)

    status = Column(Integer, nullable=False, default=0)
    force_logout = Column(Integer, nullable=False, default=0)
    device_locked = Column(Integer, nullable=False, default=0)

    current_device_id = Column(Integer, nullable=True)

    failed_login_attempts = Column(Integer, nullable=False, default=0)
    last_failed_login = Column(DateTime, nullable=True)

    user_level = Column(Integer, nullable=False, default=0)

    dept_id = Column(String(50), nullable=True)
    privileges = Column(String(200), nullable=False)

    date_time = Column(DateTime, nullable=False)

    date_modified = Column(DateTime, nullable=False)

    remote_ip = Column(String(16), nullable=False)

    originalPsd = Column(String(50), nullable=True)

    logged_in_dt = Column(DateTime, nullable=True)
    logged_out_dt = Column(DateTime, nullable=True)

    photo = Column(
        String(255),
        nullable=True,
        default="default_avatar.png"
    )

    last_group_read_at = Column(DateTime, nullable=True)

    is_super_admin = Column(Integer, nullable=True, default=0)