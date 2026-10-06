from sqlalchemy import Column, Integer, String, Text, CHAR
from database import Base

class EnDefineProfile(Base):
    __tablename__ = "en_defineprofile"

    defineprofile_id = Column(Integer, primary_key=True, autoincrement=True)
    register_id = Column(Integer, nullable=False, index=True)
    profile_id = Column(String(50), nullable=False, index=True)
    gender = Column(CHAR(1), nullable=False, index=True)

    minage = Column(Integer, nullable=False, index=True)
    maxage = Column(Integer, nullable=False, index=True)
    minheight_id = Column(Integer, nullable=False, index=True)
    maxheight_id = Column(Integer, nullable=False, index=True)

    minweight = Column(Integer, nullable=False)
    maxweight = Column(Integer, nullable=False)

    complextion = Column(String(200), nullable=True)

    qualification_id = Column(String(500), nullable=True, index=True)
    partner_qualification = Column(Text, nullable=False)

    occupation_id = Column(String(1000), nullable=True)

    religion_id = Column(Integer, nullable=False, index=True)
    denomination = Column(Integer, nullable=True)
    religiousvalue = Column(Integer, nullable=True)

    caste_id = Column(Integer, nullable=False, index=True)
    subcaste = Column(String(50), nullable=False)

    citizenship = Column(String(500), nullable=True)

    lifestyle = Column(Text, nullable=True)
    partnerdiet = Column(String(50), nullable=True)
    partnersmoke = Column(String(50), nullable=True)
    partnerdrink = Column(Integer, nullable=False)

    otherinfo = Column(Text, nullable=False)

    datecreated = Column(Integer, nullable=False)
    datemodified = Column(Integer, nullable=False)

    status = Column(Integer, nullable=True, default=1, index=True)
    deleted = Column(Integer, nullable=True, default=0, index=True)

    height_id_FK = Column(Integer, nullable=False, default=1, index=True)

    marital_status = Column(String(20), nullable=True, index=True)

    caste_more = Column(Text, nullable=True)

    annualincome_id = Column(String(50), nullable=True)
    annualincome = Column(String(255), nullable=True)

    state_id = Column(Text, nullable=True, index=True)
    state_other = Column(String(45), nullable=True)

    residing_city = Column(String(250), nullable=True)
    residing_other_city = Column(String(255), nullable=True)

    partner_family_type = Column(String(45), nullable=True)

    willing_tomarryothres_cast = Column(String(1), nullable=True)

    partner_hobbiles = Column(String(45), nullable=True)
    partner_interests = Column(Text, nullable=True)
    partner_interests_pets = Column(Text, nullable=True)
    partner_interest_assets = Column(Text, nullable=True)
