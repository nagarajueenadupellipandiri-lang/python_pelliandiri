from sqlalchemy import Column, Integer, String, Text, Date, DateTime, CHAR, Boolean
from database import Base


class EngRegister(Base):
    __tablename__ = "en_register"

    register_id = Column(Integer, primary_key=True, autoincrement=True)

    profile_id = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    dob = Column(Integer, nullable=False)
    tob = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

    gender = Column(String(1), nullable=False)
    maritialstatus = Column(Integer, nullable=False, default=1)
    childstatus = Column(String(2), nullable=False, default="N")

    religion_id = Column(Integer, nullable=False)
    denomination = Column(Integer, nullable=False, default=0)
    caste_id = Column(Integer, nullable=False)
    subcaste = Column(String(50), nullable=False)

    religiousvalue = Column(Integer, nullable=True)

    citizenship = Column(Integer, nullable=False)
    livingin = Column(Integer, nullable=False)

    state_id = Column(Integer, nullable=False)
    state_other = Column(String(50), nullable=False)

    permnt_state_id = Column(Integer, nullable=True)
    residing_city = Column(String(1000), nullable=True)
    residing_other_city = Column(String(255), nullable=True)

    hasphoto = Column(Integer, nullable=False, default=0)
    hasvideo = Column(Integer, nullable=True, default=0)
    photopassword = Column(String(50), nullable=False)

    isprotected = Column(Integer, nullable=False, default=0)
    hasastro = Column(Integer, nullable=False, default=0)

    datecreated = Column(Integer, nullable=False)
    datemodified = Column(Integer, nullable=True)
    last_visited = Column(Integer, nullable=True)

    valid_upto = Column(Integer, nullable=False)
    valid_upto_time = Column(String(100), nullable=False)
    grace_time = Column(String(150), nullable=False)

    date_deactivated = Column(Date, nullable=False)

    date_rejected = Column(Integer, nullable=True)
    date_hold = Column(Integer, nullable=True)
    date_deleted = Column(Integer, nullable=True)
    date_autodeactivated = Column(Integer, nullable=True)

    member_status = Column(Integer, nullable=False, default=0)
    featured_member = Column(Integer, nullable=False, default=0)

    ignore_list = Column(Text, nullable=True)
    block_list = Column(Text, nullable=True)

    isactive = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=1)
    deleted = Column(Integer, nullable=False, default=0)

    expressinterest = Column(Integer, nullable=False, default=0)
    viewcount = Column(Integer, nullable=False, default=0)

    generated_password = Column(String(10), nullable=False)

    date_activated = Column(Integer, nullable=True)
    loginstatus = Column(Integer, nullable=False)

    view_contacts_limit = Column(Integer, nullable=False)
    pm_limit = Column(Integer, nullable=False)

    registered_ip = Column(String(50), nullable=True)

    PV_status = Column(Integer, nullable=True)

    agent_emp_details = Column(String(50), nullable=True)
    agent_emp_name = Column(String(50), nullable=True)
    agent_emp_area = Column(String(50), nullable=True)
    agent_emp_code = Column(String(50), nullable=True)
    agent_emp_mobile = Column(Integer, nullable=True)
    agent_emp_date = Column(Integer, nullable=True)

    enrolled_by = Column(String(5), nullable=True)
    register_from = Column(String(10), nullable=False, default="WEB")

    offline_empid = Column(String(45), nullable=True)
    offline_empname = Column(String(100), nullable=True)
    offline_empremarks = Column(Text, nullable=True)

    facebiik_link = Column(Text, nullable=True)
    linkedin_link = Column(Text, nullable=True)

    privacy_access = Column(Integer, nullable=False, default=0)

    temp_country = Column(Integer, nullable=True)
    temp_state = Column(String(50), nullable=True)
    temp_city = Column(String(50), nullable=True)
    temp_town = Column(String(45), nullable=True)
    temp_pincode = Column(String(6), nullable=True)

    pincode = Column(String(6), nullable=True)
    town = Column(String(45), nullable=True)

    is_temp_perment_same = Column(Integer, nullable=True, default=0)

    referred_regid = Column(String(255), nullable=True)
    referred_Cnt = Column(Integer, nullable=True, default=0)

    adons_type = Column(String(5), nullable=True)
    adons_id = Column(String(5), nullable=True)
    adons_valid_upto = Column(Date, nullable=True)

    no_of_times = Column(Integer, nullable=True)

    is_consented = Column(Boolean, nullable=True, default=False)
    consent_date = Column(DateTime, nullable=True)

    assigned_to = Column(Integer, nullable=True)
    assigned_by = Column(Integer, nullable=True)
