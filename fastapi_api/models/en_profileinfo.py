from sqlalchemy import Column, Integer, String, Text, CHAR, ForeignKey
from database import Base


class EnProfileInfo(Base):
    __tablename__ = "en_profileinfo"

    profileinfo_id = Column(Integer, primary_key=True, autoincrement=True)
    register_id = Column(
        Integer,
        ForeignKey("en_register.register_id"),
        nullable=False,
        index=True
    )
    bloodgroup = Column(String(10), nullable=True)
    height_id = Column(Integer, nullable=False, index=True)
    weight = Column(Integer, nullable=False)
    bodytype = Column(String(20), nullable=False)
    physicalstatus = Column(CHAR(1), nullable=False)
    complextion = Column(String(15), nullable=False)

    mothertongue = Column(Integer, nullable=False, index=True)
    can_speak = Column(String(50), nullable=False)
    can_speak_lang = Column(String(100), nullable=False)
    placeofbirth = Column(String(50), nullable=False)

    diet = Column(Integer, nullable=True)
    smoke = Column(Integer, nullable=True)
    drink = Column(Integer, nullable=True)

    star_id = Column(Integer, nullable=True, index=True)
    raasi_id = Column(Integer, nullable=True, index=True)

    gothram = Column(String(50), nullable=False)
    manglik = Column(Integer, nullable=True)

    qualification_id = Column(Integer, nullable=False, index=True)
    discipline_id = Column(Integer, nullable=True, index=True)
    occupation_id = Column(Integer, nullable=False, index=True)

    designation = Column(String(50), nullable=False)
    employed_in = Column(Text, nullable=False)
    employment_location = Column(Text, nullable=False)
    occupation_details = Column(String(50), nullable=True)

    qualification = Column(String(150), nullable=False)

    annualincome_id = Column(Integer, nullable=False, index=True)
    annualincome = Column(String(50), nullable=False)

    residingstatus_code = Column(CHAR(1), nullable=False)

    email = Column(String(100), nullable=False, index=True)
    email_display_status = Column(Integer, nullable=False, default=0)

    mobile = Column(String(20), nullable=False, index=True)
    mobile_display_status = Column(Integer, nullable=False, default=0)

    countrycode = Column(String(10), nullable=False)
    areacode = Column(Integer, nullable=True)
    phoneno = Column(String(10), nullable=True)
    phone_display_status = Column(Integer, nullable=False, default=0)

    family_values = Column(String(30), nullable=True)
    family_type = Column(String(30), nullable=True)
    family_status = Column(String(30), nullable=True)

    family_brothers_married = Column(Integer, nullable=True)
    family_brothers_unmarried = Column(Integer, nullable=True)
    family_sisters_married = Column(Integer, nullable=True)
    family_sisters_unmarried = Column(Integer, nullable=True)

    profile_summary = Column(Text, nullable=True)
    interest_hobbies = Column(Text, nullable=False)
    family_details = Column(Text, nullable=False)

    desc_flag = Column(Integer, nullable=True, default=0)

    contact_person = Column(String(50), nullable=False)
    contact_address = Column(Text, nullable=False)
    contact_relationship = Column(String(100), nullable=True)

    reference1_name = Column(String(50), nullable=False)
    reference1_tele = Column(String(20), nullable=False)
    reference1_address = Column(Text, nullable=False)

    reference2_name = Column(String(50), nullable=False)
    reference2_tele = Column(String(20), nullable=False)
    reference2_address = Column(Text, nullable=False)

    registerby = Column(String(15), nullable=False)

    status = Column(Integer, nullable=True, default=1)
    deleted = Column(Integer, nullable=True, default=0)

    father_occupation_id = Column(Integer, nullable=True)
    mother_occupation_id = Column(Integer, nullable=True)

    college = Column(Text, nullable=True)
    university = Column(String(45), nullable=True)
    placeofstudy = Column(String(45), nullable=True)
    yearofpassing = Column(String(45), nullable=True)

    total_work_experiance = Column(String(45), nullable=True)

    family_members = Column(String(45), nullable=True)
    family_income = Column(String(45), nullable=True)
    family_hometown = Column(String(45), nullable=True)
    family_livingcity = Column(String(45), nullable=True)

    hobbies = Column(String(45), nullable=True)
    interests = Column(Text, nullable=True)
    assets = Column(Text, nullable=True)
    about_me = Column(Text, nullable=True)

    interest_on_pets = Column(String(45), nullable=True)
    health_info = Column(String(45), nullable=True)
    about_physical_status = Column(Text, nullable=True)

    specialization = Column(String(45), nullable=True)
    company_name = Column(String(45), nullable=True)

    father_name = Column(String(45), nullable=True)
    mother_name = Column(String(45), nullable=True)

    other_contact_person = Column(String(50), nullable=True)

    other_contact_person_relation = Column(
        "other_contact_person_relation_to_bride/groom",
        String(50),
        nullable=True
    )

    other_contact_person_phonenum = Column(String(45), nullable=True)
    other_contact_person_address = Column(Text, nullable=True)

    is_email_verified = Column(String(2), nullable=True, index=True)

    family_incometype = Column(Integer, nullable=True, default=0)
