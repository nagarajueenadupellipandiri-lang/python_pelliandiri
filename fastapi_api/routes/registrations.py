from datetime import datetime, date
from fastapi import APIRouter, Depends
from hashlib import md5
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db
from models import EngRegister, EnProfileInfo
from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/registrations", tags=["Registrations"] )

@router.post("/getRegistartions")
def get_registrations(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")

    params = request.params or {}

    try:
        page = int(params.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    try:
        limit = int(params.get("limit", 50))
    except (TypeError, ValueError):
        limit = 50

    if page < 1:
        page = 1

    if limit < 1:
        limit = 50

    if limit > 100:
        limit = 100

    search = params.get("search", "")

    if search is None:
        search = ""

    search = str(search).strip()

    # -----------------------------------------
    # JOIN en_register + en_profileinfo
    # -----------------------------------------
    query = (
        db.query(
            EngRegister,
            EnProfileInfo
        )
        .outerjoin(
            EnProfileInfo,
            EngRegister.register_id == EnProfileInfo.register_id
        )
    )

    # -----------------------------------------
    # Search
    # -----------------------------------------
    if search:
        search_value = f"%{search}%"

        query = query.filter(
            or_(
                EngRegister.profile_id.ilike(search_value),
                EngRegister.name.ilike(search_value),
                EnProfileInfo.email.ilike(search_value),
                EnProfileInfo.mobile.ilike(search_value)
            )
        )

    # -----------------------------------------
    # Total count
    # -----------------------------------------

    total_registrations = query.with_entities(
        func.count(EngRegister.register_id)
    ).scalar()

    total_registrations = total_registrations or 0

    total_pages = (
        (total_registrations + limit - 1) // limit
        if total_registrations > 0
        else 0
    )

    # -----------------------------------------
    # Pagination
    # -----------------------------------------

    offset = (page - 1) * limit

    registrations = (
        query
        .order_by(EngRegister.register_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # -----------------------------------------
    # Response data
    # -----------------------------------------

    data = []

    for reg, profile in registrations:

        data.append({
            # en_register
            "register_id": reg.register_id,
            "profile_id": reg.profile_id,
            "name": reg.name,
            "dob": reg.dob,
            "tob": reg.tob,
            "age": reg.age,
            "gender": reg.gender,
            "maritialstatus": reg.maritialstatus,
            "childstatus": reg.childstatus,

            "religion_id": reg.religion_id,
            "denomination": reg.denomination,
            "caste_id": reg.caste_id,
            "subcaste": reg.subcaste,

            "citizenship": reg.citizenship,
            "livingin": reg.livingin,

            "state_id": reg.state_id,
            "state_other": reg.state_other,

            "permnt_state_id": reg.permnt_state_id,
            "residing_city": reg.residing_city,
            "residing_other_city": reg.residing_other_city,

            "temp_country": reg.temp_country,
            "temp_state": reg.temp_state,
            "temp_city": reg.temp_city,
            "temp_town": reg.temp_town,
            "temp_pincode": reg.temp_pincode,

            "pincode": reg.pincode,
            "town": reg.town,

            "status": reg.status,
            "deleted": reg.deleted,
            "isactive": reg.isactive,

            # en_profileinfo
            "profileinfo_id": profile.profileinfo_id if profile else None,

            "bloodgroup": profile.bloodgroup if profile else None,
            "height_id": profile.height_id if profile else None,
            "weight": profile.weight if profile else None,
            "bodytype": profile.bodytype if profile else None,
            "physicalstatus": profile.physicalstatus if profile else None,
            "complextion": profile.complextion if profile else None,

            "mothertongue": profile.mothertongue if profile else None,
            "can_speak": profile.can_speak if profile else None,
            "can_speak_lang": profile.can_speak_lang if profile else None,
            "placeofbirth": profile.placeofbirth if profile else None,

            "star_id": profile.star_id if profile else None,
            "raasi_id": profile.raasi_id if profile else None,
            "gothram": profile.gothram if profile else None,

            "qualification_id": profile.qualification_id if profile else None,
            "discipline_id": profile.discipline_id if profile else None,
            "occupation_id": profile.occupation_id if profile else None,

            "designation": profile.designation if profile else None,
            "employed_in": profile.employed_in if profile else None,
            "employment_location": (
                profile.employment_location
                if profile else None
            ),

            "occupation_details": (
                profile.occupation_details
                if profile else None
            ),

            "qualification": (
                profile.qualification
                if profile else None
            ),

            "annualincome_id": (
                profile.annualincome_id
                if profile else None
            ),

            "annualincome": (
                profile.annualincome
                if profile else None
            ),

            "residingstatus_code": (
                profile.residingstatus_code
                if profile else None
            ),

            "email": profile.email if profile else None,
            "email_display_status": (
                profile.email_display_status
                if profile else None
            ),

            "mobile": profile.mobile if profile else None,
            "mobile_display_status": (
                profile.mobile_display_status
                if profile else None
            ),

            "countrycode": (
                profile.countrycode
                if profile else None
            ),

            "profile_status": (
                profile.status
                if profile else None
            ),
        })

    return {
        "status": True,
        "message": "Registrations fetched successfully",
        "pagination": {
            "page": page,
            "limit": limit,
            "total_registrations": total_registrations,
            "total_pages": total_pages,
        },
        "search": search,
        "data": data,
    }

@router.post("/createRegistartion")
def new_registartion(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # =========================================================
    # 1. VALIDATE COMMON REQUEST
    # =========================================================
    validate_common_request(request, "login")

    params = request.params or {}

    # =========================================================
    # 2. REQUIRED REGISTRATION FIELDS
    # =========================================================
    name = params.get("name")
    gender = params.get("gender")
    dob = params.get("dob")

    maritialstatus = params.get("maritialstatus")
    religion_id = params.get("religion_id")
    caste_id = params.get("caste_id")
    citizenship = params.get("citizenship")
    livingin = params.get("livingin")
    state_id = params.get("state_id")

    # =========================================================
    # 3. OPTIONAL REGISTRATION FIELDS
    # =========================================================
    tob = params.get("tob")
    childstatus = params.get("childstatus")
    denomination = params.get("denomination", 0)

    subcaste = params.get("subcaste")
    state_other = params.get("state_other", "")

    registerby = params.get("registerby")

    # =========================================================
    # 4. REQUIRED FIELD VALIDATION
    # =========================================================
    required_fields = {
        "name": name,
        "gender": gender,
        "dob": dob,
        "maritialstatus": maritialstatus,
        "religion_id": religion_id,
        "caste_id": caste_id,
        "citizenship": citizenship,
        "livingin": livingin,
        "state_id": state_id,
    }

    for field, value in required_fields.items():
        if value is None or str(value).strip() == "":
            return {
                "status": False,
                "message": f"{field} is required"
            }

    try:

        birth_date = datetime.strptime(
            str(dob),
            "%Y-%m-%d"
        ).date()

        today = date.today()

        age = today.year - birth_date.year

        if (today.month, today.day) < (
            birth_date.month,
            birth_date.day
        ):
            age -= 1

        if age < 0 or age > 150:
            return {
                "status": False,
                "message": "Invalid date of birth"
            }

        dob = int(
            datetime.combine(
                birth_date,
                datetime.min.time()
            ).timestamp()
        )

    except (
        ValueError,
        TypeError,
        OverflowError,
        OSError
    ):

        return {
            "status": False,
            "message": "dob must be in YYYY-MM-DD format"
        }

    # =========================================================
    # 6. VALIDATE GENDER
    # =========================================================

    gender = str(gender).upper().strip()

    if gender not in ["M", "F"]:

        return {
            "status": False,
            "message": "Gender must be M or F"
        }

    # =========================================================
    # 7. CONVERT REQUIRED NUMERIC FIELDS
    # =========================================================

    try:

        religion_id = int(religion_id)
        denomination = int(denomination)
        caste_id = int(caste_id)
        citizenship = int(citizenship)
        livingin = int(livingin)
        state_id = int(state_id)
        maritialstatus = int(maritialstatus)

    except (TypeError, ValueError):

        return {
            "status": False,
            "message": "Invalid numeric value in required fields"
        }

    # =========================================================
    # 8. OPTIONAL PROFILE FIELDS
    # =========================================================

    height_id = params.get("height_id")
    weight = params.get("weight")

    if weight in [None, ""]:
        weight = 0
    else:
        try:
            weight = int(weight)
        except (TypeError, ValueError):
            return {
                "status": False,
                "message": "weight must be a number"
            }
            
    bodytype = params.get("bodytype")
    physicalstatus = params.get("physicalstatus")
    complextion = params.get("complextion")

    mothertongue = params.get("mothertongue")
    can_speak = params.get("can_speak")
    can_speak_lang = params.get("can_speak_lang")

    placeofbirth = params.get("placeofbirth")

    star_id = params.get("star_id")
    raasi_id = params.get("raasi_id")
    gothram = params.get("gothram")

    qualification_id = params.get("qualification_id")
    discipline_id = params.get("discipline_id")
    occupation_id = params.get("occupation_id")

    designation = params.get("designation")
    employed_in = params.get("employed_in")
    employment_location = params.get("employment_location")
    occupation_details = params.get("occupation_details")

    qualification = params.get("qualification")

    annualincome_id = params.get("annualincome_id")
    annualincome = params.get("annualincome")

    residingstatus_code = params.get("residingstatus_code")

    email = params.get("email")
    mobile = params.get("mobile")
    countrycode = params.get("countrycode")

    # =========================================================
    # 9. OPTIONAL FAMILY FIELDS
    # =========================================================
    family_brothers_married = int(params.get("family_brothers_married") or 0)
    family_brothers_unmarried = int(params.get("family_brothers_unmarried") or 0)
    family_sisters_married = int(params.get("family_sisters_married") or 0)
    family_sisters_unmarried = int(params.get("family_sisters_unmarried") or 0)


    family_livingcity = params.get(
        "family_livingcity"
    )

    family_hometown = params.get(
        "family_hometown"
    )

    family_income = params.get(
        "family_income"
    )

    family_members = params.get(
        "family_members"
    )

    # =========================================================
    # 10. OPTIONAL EDUCATION / WORK FIELDS
    # =========================================================

    father_occupation_id = params.get(
        "father_occupation_id"
    )

    mother_occupation_id = params.get(
        "mother_occupation_id"
    )

    father_name = params.get(
        "father_name"
    )

    mother_name = params.get(
        "mother_name"
    )

    college = params.get(
        "college"
    )

    university = params.get(
        "university"
    )

    placeofstudy = params.get(
        "placeofstudy"
    )

    yearofpassing = params.get(
        "yearofpassing"
    )

    total_work_experiance = params.get(
        "total_work_experiance"
    )

    specialization = params.get(
        "specialization"
    )

    company_name = params.get(
        "company_name"
    )

    # =========================================================
    # 11. OPTIONAL CONTACT FIELDS
    # =========================================================

    other_contact_person = params.get(
        "other_contact_person"
    )

    other_contact_person_relation = params.get(
        "other_contact_person_relation"
    )

    other_contact_person_phonenum = params.get(
        "other_contact_person_phonenum"
    )

    other_contact_person_address = params.get(
        "other_contact_person_address"
    )

    # =========================================================
    # 12. OPTIONAL LOCATION FIELDS
    # =========================================================

    permnt_state_id = params.get(
        "permnt_state_id"
    )

    residing_city = params.get(
        "residing_city"
    )

    residing_other_city = params.get(
        "residing_other_city"
    )

    temp_country = params.get(
        "temp_country"
    )

    temp_state = params.get(
        "temp_state"
    )

    temp_city = params.get(
        "temp_city"
    )

    temp_town = params.get(
        "temp_town"
    )

    temp_pincode = params.get(
        "temp_pincode"
    )

    # =========================================================
    # 13. OPTIONAL NUMERIC CONVERSION
    # =========================================================

    try:

        height_id = (
            int(height_id)
            if height_id not in [None, ""]
            else None
        )

        weight = (
            int(weight)
            if weight not in [None, ""]
            else None
        )

        bodytype = (
            int(bodytype)
            if bodytype not in [None, ""]
            else None
        )

        physicalstatus = (
            int(physicalstatus)
            if physicalstatus not in [None, ""]
            else None
        )

        complextion = (
            int(complextion)
            if complextion not in [None, ""]
            else None
        )

        mothertongue = (
            int(mothertongue)
            if mothertongue not in [None, ""]
            else None
        )

        can_speak = (
            int(can_speak)
            if can_speak not in [None, ""]
            else None
        )

        can_speak_lang = (
            int(can_speak_lang)
            if can_speak_lang not in [None, ""]
            else None
        )

        star_id = (
            int(star_id)
            if star_id not in [None, ""]
            else None
        )

        raasi_id = (
            int(raasi_id)
            if raasi_id not in [None, ""]
            else None
        )

        qualification_id = (
            int(qualification_id)
            if qualification_id not in [None, ""]
            else None
        )

        discipline_id = (
            int(discipline_id)
            if discipline_id not in [None, ""]
            else None
        )

        occupation_id = (
            int(occupation_id)
            if occupation_id not in [None, ""]
            else None
        )

        annualincome_id = (
            int(annualincome_id)
            if annualincome_id not in [None, ""]
            else None
        )

        residingstatus_code = (
            int(residingstatus_code)
            if residingstatus_code not in [None, ""]
            else None
        )

        father_occupation_id = (
            int(father_occupation_id)
            if father_occupation_id not in [None, ""]
            else None
        )

        mother_occupation_id = (
            int(mother_occupation_id)
            if mother_occupation_id not in [None, ""]
            else None
        )

        yearofpassing = (
            int(yearofpassing)
            if yearofpassing not in [None, ""]
            else None
        )

        total_work_experiance = (
            int(total_work_experiance)
            if total_work_experiance not in [None, ""]
            else None
        )

    except (TypeError, ValueError):

        return {
            "status": False,
            "message": "Invalid optional numeric value"
        }

    # =========================================================
    # 14. EMAIL
    # =========================================================

    email = (
        str(email).strip()
        if email is not None
        else ""
    )

    # IMPORTANT:
    # Always initialize variable.
    existing_email = None

    if email:

        existing_email = (
            db.query(EnProfileInfo)
            .filter(
                EnProfileInfo.email == email
            )
            .first()
        )

        if existing_email:

            return {
                "status": False,
                "message": "Email already exists"
            }

    # =========================================================
    # 15. MOBILE DUPLICATE CHECK
    # =========================================================

    existing_mobile = None

    print("====================================")
    print("MOBILE FROM REQUEST:", repr(mobile))
    print("DB URL:", db.bind.url)
    print("====================================")
    if mobile:

        existing_mobile = (
            db.query(EnProfileInfo)
            .filter(
                EnProfileInfo.mobile == mobile
            )
            .first()
        )

        if existing_mobile:

            return {
                "status": False,
                "message": "Mobile already exists"
            }

    # =========================================================
    # 16. CURRENT TIMESTAMP
    # =========================================================

    current_timestamp = int(
        datetime.now().timestamp()
    )

    temporary_profile_id = (
        f"TEMP-{int(datetime.now().timestamp() * 1000000)}"
    )

    # =========================================================
    # 17. DATABASE INSERT
    # =========================================================

    try:

        registration = EngRegister(

            profile_id=temporary_profile_id,

            name=name,

            password="",
            photopassword="",
            generated_password="",

            dob=dob,

            tob=tob,

            age=age,

            gender=gender,

            maritialstatus=maritialstatus,

            childstatus=childstatus,

            religion_id=religion_id,

            denomination=denomination,

            caste_id=caste_id,

            subcaste=subcaste,

            citizenship=citizenship,

            livingin=livingin,

            state_id=state_id,

            state_other=state_other,

            hasphoto=0,

            hasvideo=0,

            isprotected=0,

            hasastro=0,

            datecreated=current_timestamp,

            datemodified=None,

            last_visited=None,

            valid_upto=current_timestamp,

            valid_upto_time="",

            grace_time="",

            date_deactivated=date(1970, 1, 1),

            date_rejected=None,

            date_hold=None,

            date_deleted=None,

            date_autodeactivated=None,

            member_status=0,

            featured_member=0,

            ignore_list=None,

            block_list=None,

            isactive=0,

            status=1,

            deleted=0,

            expressinterest=0,

            viewcount=0,

            date_activated=None,

            loginstatus=0,

            view_contacts_limit=0,

            pm_limit=0,

            registered_ip=None,

            PV_status=None,

            agent_emp_details=None,

            agent_emp_name=None,

            agent_emp_area=None,

            agent_emp_code=None,

            agent_emp_mobile=None,

            agent_emp_date=None,

            enrolled_by=None,

            register_from="WEB",

            offline_empid=None,

            offline_empname=params.get(
                "offline_empname"
            ),

            offline_empremarks=None,

            facebiik_link=None,

            linkedin_link=None,

            privacy_access=0,

            temp_country=temp_country,

            temp_state=temp_state,

            temp_city=temp_city,

            temp_town=temp_town,

            temp_pincode=temp_pincode,

            pincode=None,

            town=None,

            is_temp_perment_same=0,

            referred_regid=None,

            referred_Cnt=0,

            adons_type=None,

            adons_id=None,

            adons_valid_upto=None,

            no_of_times=None,

            is_consented=False,

            consent_date=None,

            assigned_to=None,

            assigned_by=None
        )

        # =====================================================
        # 18. SAVE REGISTER
        # =====================================================

        db.add(registration)

        db.flush()

        register_id = registration.register_id

        profile_id = f"EP{register_id:06d}"

        registration.profile_id = profile_id

        # =====================================================
        # 19. CREATE PROFILE INFO
        # =====================================================

        profile_info = EnProfileInfo(

            register_id=register_id,

            height_id=height_id,

            weight=weight,

            bodytype=bodytype,

            physicalstatus=physicalstatus,

            complextion=complextion,

            mothertongue=mothertongue,

            can_speak=can_speak,

            can_speak_lang=can_speak_lang,

            placeofbirth=placeofbirth,

            star_id=star_id,

            raasi_id=raasi_id,

            gothram=gothram,

            qualification_id=qualification_id,

            discipline_id=discipline_id,

            occupation_id=occupation_id,

            designation=designation,

            employed_in=employed_in,

            employment_location=employment_location,

            occupation_details=occupation_details,

            qualification=qualification,

            annualincome_id=annualincome_id,

            annualincome=annualincome,

            residingstatus_code=residingstatus_code,

            email=email,

            email_display_status=0,

            mobile=mobile,

            mobile_display_status=0,

            countrycode=countrycode,

            areacode=None,

            phoneno=None,

            phone_display_status=0,

            family_values=None,

            family_type=None,

            family_status=None,

            family_brothers_married=family_brothers_married,

            family_brothers_unmarried=family_brothers_unmarried,

            family_sisters_married=family_sisters_married,

            family_sisters_unmarried=family_sisters_unmarried,

            profile_summary=None,

            interest_hobbies="",

            family_details="",

            desc_flag=0,

            contact_person="",

            contact_address="",

            contact_relationship=None,

            registerby=registerby,

            status=1,

            deleted=0,

            father_occupation_id=father_occupation_id,

            mother_occupation_id=mother_occupation_id,

            college=college,

            university=university,

            placeofstudy=placeofstudy,

            yearofpassing=yearofpassing,

            total_work_experiance=total_work_experiance,

            family_members=family_members,

            family_income=family_income,

            family_hometown=family_hometown,

            family_livingcity=family_livingcity,

            hobbies=None,

            interests=None,

            assets=None,

            about_me=None,

            interest_on_pets=None,

            health_info=None,

            about_physical_status=params.get(
                "about_physical_status"
            ),

            specialization=specialization,

            company_name=company_name,

            father_name=father_name,

            mother_name=mother_name,

            other_contact_person=other_contact_person,

            other_contact_person_relation=(
                other_contact_person_relation
            ),

            other_contact_person_phonenum=(
                other_contact_person_phonenum
            ),

            other_contact_person_address=(
                other_contact_person_address
            ),

            # ================================
            reference1_name="",
            reference1_tele="",
            reference1_address="",

            reference2_name="",
            reference2_tele="",
            reference2_address="",
            # ==============================


            is_email_verified=None,

            family_incometype=0
        )

        # =====================================================
        # 20. SAVE PROFILE
        # =====================================================

        db.add(profile_info)

        db.commit()

        db.refresh(registration)

        db.refresh(profile_info)

    except Exception as e:

        db.rollback()

        return {
            "status": False,
            "message": "Unable to create registration",
            "error": str(e)
        }

    # =========================================================
    # 21. RESPONSE
    # =========================================================

    return {

        "status": True,

        "message": "Registration created successfully",

        "data": {

            "register": {

                "register_id": registration.register_id,

                "profile_id": registration.profile_id,

                "name": registration.name,

                "gender": registration.gender,

                "dob": registration.dob,

                "tob": registration.tob,

                "age": registration.age,

                "maritialstatus": registration.maritialstatus,

                "childstatus": registration.childstatus,

                "religion_id": registration.religion_id,

                "denomination": registration.denomination,

                "caste_id": registration.caste_id,

                "subcaste": registration.subcaste,

                "citizenship": registration.citizenship,

                "livingin": registration.livingin,

                "state_id": registration.state_id,

                "state_other": registration.state_other,

                "hasphoto": registration.hasphoto,

                "hasvideo": registration.hasvideo,

                "isprotected": registration.isprotected,

                "hasastro": registration.hasastro,

                "datecreated": registration.datecreated,

                "valid_upto": registration.valid_upto,

                "member_status": registration.member_status,

                "featured_member": registration.featured_member,

                "isactive": registration.isactive,

                "status": registration.status,

                "deleted": registration.deleted,

                "expressinterest": registration.expressinterest,

                "viewcount": registration.viewcount,

                "loginstatus": registration.loginstatus,

                "register_from": registration.register_from,

                "privacy_access": registration.privacy_access,

                "temp_country": registration.temp_country,

                "temp_state": registration.temp_state,

                "temp_city": registration.temp_city,

                "temp_town": registration.temp_town,

                "temp_pincode": registration.temp_pincode,

                "pincode": registration.pincode,

                "town": registration.town,

                "is_temp_perment_same": (
                    registration.is_temp_perment_same
                ),

                "referred_regid": (
                    registration.referred_regid
                ),

                "referred_Cnt": (
                    registration.referred_Cnt
                ),

                "is_consented": (
                    registration.is_consented
                ),

                "consent_date": (
                    registration.consent_date
                ),

                "assigned_to": (
                    registration.assigned_to
                ),

                "assigned_by": (
                    registration.assigned_by
                )
            },

            "profile_info": {

                "profileinfo_id": (
                    profile_info.profileinfo_id
                ),

                "register_id": (
                    profile_info.register_id
                ),

                "height_id": profile_info.height_id,

                "weight": profile_info.weight,

                "bodytype": profile_info.bodytype,

                "physicalstatus": (
                    profile_info.physicalstatus
                ),

                "complextion": (
                    profile_info.complextion
                ),

                "mothertongue": (
                    profile_info.mothertongue
                ),

                "can_speak": (
                    profile_info.can_speak
                ),

                "can_speak_lang": (
                    profile_info.can_speak_lang
                ),

                "placeofbirth": (
                    profile_info.placeofbirth
                ),

                "star_id": profile_info.star_id,

                "raasi_id": profile_info.raasi_id,

                "gothram": profile_info.gothram,

                "qualification_id": (
                    profile_info.qualification_id
                ),

                "discipline_id": (
                    profile_info.discipline_id
                ),

                "occupation_id": (
                    profile_info.occupation_id
                ),

                "designation": (
                    profile_info.designation
                ),

                "employed_in": (
                    profile_info.employed_in
                ),

                "employment_location": (
                    profile_info.employment_location
                ),

                "occupation_details": (
                    profile_info.occupation_details
                ),

                "qualification": (
                    profile_info.qualification
                ),

                "annualincome_id": (
                    profile_info.annualincome_id
                ),

                "annualincome": (
                    profile_info.annualincome
                ),

                "residingstatus_code": (
                    profile_info.residingstatus_code
                ),

                "email": profile_info.email,

                "mobile": profile_info.mobile,

                "countrycode": (
                    profile_info.countrycode
                ),

                "family_brothers_married": (
                    profile_info.family_brothers_married
                ),

                "family_brothers_unmarried": (
                    profile_info.family_brothers_unmarried
                ),

                "family_sisters_married": (
                    profile_info.family_sisters_married
                ),

                "family_sisters_unmarried": (
                    profile_info.family_sisters_unmarried
                ),

                "registerby": profile_info.registerby,

                "father_occupation_id": (
                    profile_info.father_occupation_id
                ),

                "mother_occupation_id": (
                    profile_info.mother_occupation_id
                ),

                "college": profile_info.college,

                "university": profile_info.university,

                "placeofstudy": (
                    profile_info.placeofstudy
                ),

                "yearofpassing": (
                    profile_info.yearofpassing
                ),

                "total_work_experiance": (
                    profile_info.total_work_experiance
                ),

                "family_members": (
                    profile_info.family_members
                ),

                "family_income": (
                    profile_info.family_income
                ),

                "family_hometown": (
                    profile_info.family_hometown
                ),

                "family_livingcity": (
                    profile_info.family_livingcity
                ),

                "specialization": (
                    profile_info.specialization
                ),

                "company_name": (
                    profile_info.company_name
                ),

                "father_name": (
                    profile_info.father_name
                ),

                "mother_name": (
                    profile_info.mother_name
                ),

                "other_contact_person": (
                    profile_info.other_contact_person
                ),

                "other_contact_person_relation": (
                    profile_info.other_contact_person_relation
                ),

                "other_contact_person_phonenum": (
                    profile_info.other_contact_person_phonenum
                ),

                "other_contact_person_address": (
                    profile_info.other_contact_person_address
                ),

                "about_physical_status": (
                    profile_info.about_physical_status
                ),

                "is_email_verified": (
                    profile_info.is_email_verified
                ),

                "family_incometype": (
                    profile_info.family_incometype
                )
            }
        }
    }

