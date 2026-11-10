import sys, requests, json, hashlib, logging, math, uuid
from pathlib import Path
from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from django.views.decorators.cache import never_cache

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FASTAPI_DIR = PROJECT_ROOT / "fastapi_api"

if str(FASTAPI_DIR) not in sys.path:
    sys.path.insert(0, str(FASTAPI_DIR))

from database import SessionLocal
from models import (
    EnLogin,
    EnPackageCategories,
    EnPackageSubcategories,
    EngRegister,
    EnBanners,
    EnParichayaVedika,
    EnProfileInfo,
    EnReligionMaster,
    EnCasteMaster,
)
from core.security import create_access_token

def common_payload(request):
    access_token = request.session.get("access_token")

    if not access_token:
        # return redirect("login")
        return None, None

    api_type = request.session.get("api_type")
    api_authkey = request.session.get("api_authkey")

    if not api_type or not api_authkey:
        request.session.flush()
        # return redirect("login")
        return None, None

    payload = { "type": api_type, "Authkey": api_authkey, "params": {} }
    headers = { "Authorization": f"Bearer {access_token}" }

    return payload, headers

def get_registartions_data(request):
    access_token = request.session.get("access_token")

    if not access_token:
        return (401, {}, 0, 0, 0, 0, 0)

    # --------------------------------
    # Pagination
    # --------------------------------
    try:
        page = int(request.GET.get("page", 1))
        page = max(page, 1)
    except (ValueError, TypeError):
        page = 1

    per_page = 20
    offset = (page - 1) * per_page

    db = SessionLocal()

    try:
        now = datetime.now()

        # --------------------------------
        # JOIN REGISTER + PROFILE + RELIGION + CASTE
        # --------------------------------
        query = (
            db.query(
                EngRegister,
                EnProfileInfo,
                EnReligionMaster,
                EnCasteMaster
            )
            .outerjoin(
                EnProfileInfo,
                EngRegister.register_id == EnProfileInfo.register_id
            )
            .outerjoin(
                EnReligionMaster,
                EngRegister.religion_id == EnReligionMaster.religion_id
            )
            .outerjoin(
                EnCasteMaster,
                EngRegister.caste_id == EnCasteMaster.caste_id
            )
        )

        # --------------------------------
        # Total registrations
        # --------------------------------
        total_registrations = (
            db.query(func.count(EngRegister.register_id))
            .scalar() or 0
        )

        # --------------------------------
        # Male registrations
        # --------------------------------
        male_registartions = (
            db.query(func.count(EngRegister.register_id))
            .filter(EngRegister.gender == "M")
            .scalar() or 0
        )

        # --------------------------------
        # Female registrations
        # --------------------------------
        female_registartions = (
            db.query(func.count(EngRegister.register_id))
            .filter(EngRegister.gender == "F")
            .scalar() or 0
        )

        # --------------------------------
        # Today registrations
        # --------------------------------
        today_start = int(
            now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ).timestamp()
        )

        tomorrow_start = today_start + 86400

        today_registrations = (
            db.query(func.count(EngRegister.register_id))
            .filter(
                EngRegister.datecreated >= today_start,
                EngRegister.datecreated < tomorrow_start
            )
            .scalar() or 0
        )

        # --------------------------------
        # This month registrations
        # --------------------------------
        month_start = datetime(
            now.year, now.month, 1, tzinfo=now.tzinfo
        )

        if now.month == 12:
            next_month = datetime(now.year + 1, 1, 1, tzinfo=now.tzinfo)
        else:
            next_month = datetime(
                now.year, now.month + 1, 1, tzinfo=now.tzinfo
            )

        this_month_registrations = (
            db.query(func.count(EngRegister.register_id))
            .filter(
                EngRegister.datecreated >= int(month_start.timestamp()),
                EngRegister.datecreated < int(next_month.timestamp())
            )
            .scalar() or 0
        )

        # --------------------------------
        # Pagination calculation
        # --------------------------------
        total_pages = max(
            1,
            math.ceil(total_registrations / per_page)
        )

        page = min(page, total_pages)
        offset = (page - 1) * per_page

        # --------------------------------
        # Fetch registrations with JOIN
        # --------------------------------
        registrations = (
            query
            .order_by(EngRegister.register_id.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )

        # --------------------------------
        # Convert JOIN records into dictionaries
        # --------------------------------
        register_users = []

        for reg, profile, religion, caste in registrations:

            register_users.append({

                # EngRegister
                "register_id": reg.register_id,
                "profile_id": reg.profile_id,
                "name": reg.name,
                "dob": reg.dob,
                "gender": reg.gender,
                "maritialstatus": reg.maritialstatus,

                "religion_id": reg.religion_id,
                "religion_name": ( religion.religion_name if religion else None ),
                "denomination": reg.denomination,

                "caste_id": reg.caste_id,
                "caste_name": (
                    caste.caste_name if caste else None
                ),

                "subcaste": reg.subcaste,

                "citizenship": reg.citizenship,
                "livingin": reg.livingin,

                "state_id": reg.state_id,
                "state_other": reg.state_other,

                "pincode": reg.pincode,
                "town": reg.town,

                "datecreated": reg.datecreated,

                # EnProfileInfo
                "email": profile.email if profile else None,
                "mobile": profile.mobile if profile else None,

                "bloodgroup": profile.bloodgroup if profile else None,
                "height_id": profile.height_id if profile else None,
                "weight": profile.weight if profile else None,

                "occupation_id": ( profile.occupation_id if profile else None ),
                "qualification_id": ( profile.qualification_id if profile else None ),

            })

        # print("Registration JOIN data:", register_users[:2])

        # --------------------------------
        # Final response
        # --------------------------------
        registers = {
            "data": register_users,

            "pagination": {
                "total_registrations": total_registrations,
                "current_page": page,
                "per_page": per_page,
                "total_pages": total_pages
            },

            "male_registartions": male_registartions,
            "female_registartions": female_registartions,
            "today_registrations": today_registrations,
            "this_month_registrations": this_month_registrations
        }

        return (
            200,
            registers,
            total_registrations,
            male_registartions,
            female_registartions,
            today_registrations,
            this_month_registrations
        )

    except SQLAlchemyError:
        logging.exception("Registration database error")
        return (500, {}, 0, 0, 0, 0, 0)

    finally:
        db.close()

def get_religion_list(request):
    payload, headers = common_payload(request)
    religion_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/basicInfo/religion", 
        json=payload,
        headers=headers,
        timeout=10
    )
    religions = religion_response.json()
    return religions

def get_christianDenomination_list(request):
    payload, headers = common_payload(request)
    christianDenomination_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/basicInfo/christianDenomination", 
        json=payload,
        headers=headers,
        timeout=10
    )
    christianDenomination = christianDenomination_response.json()
    return christianDenomination

def get_muslimSubsects_list(request):
    payload, headers = common_payload(request)
    muslimSubsects_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/basicInfo/muslimSubsects", 
        json=payload,
        headers=headers,
        timeout=10
    )
    muslimSubsects = muslimSubsects_response.json()
    return muslimSubsects

def get_cste_list(request):
    payload, headers = common_payload(request)
    religion_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/basicInfo/caste", 
        json=payload,
        headers=headers,
        timeout=10
    )
    castes = religion_response.json()
    return castes

def get_height_list(request):
    payload, headers = common_payload(request)
    height_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/basicInfo/height", 
        json=payload,
        headers=headers,
        timeout=10
    )
    heights = height_response.json()
    return heights

def get_education_qualification_list(request):
    payload, headers = common_payload(request)
    education_qualification_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/educationDetails/education", 
        json=payload,
        headers=headers,
        timeout=10
    )
    educationQualifications = education_qualification_response.json()
    return educationQualifications

def get_occupation_master_head_list(request):
    payload, headers = common_payload(request)
    employee_occupatipon_head_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/employmentDetails/occupationMasterHead", 
        json=payload,
        headers=headers,
        timeout=10
    )
    employeeOccupationHead = employee_occupatipon_head_response.json()
    return employeeOccupationHead

def get_occupation_list(request):
    payload, headers = common_payload(request)
    employee_occupatipon_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/employmentDetails/occupations", 
        json=payload,
        headers=headers,
        timeout=10
    )
    employeeOccupations = employee_occupatipon_response.json()
    return employeeOccupations

def get_income_list(request):
    payload, headers = common_payload(request)
    employee_income_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/employmentDetails/incomes", 
        json=payload,
        headers=headers,
        timeout=10
    )
    employeeOccupations = employee_income_response.json()
    return employeeOccupations

def get_occupation_groups(get_occupation_master_head_list, occupation_list):

    occupation_groups = []

    # ---------------------------------------
    # Create category headings
    # ---------------------------------------
    for category in get_occupation_master_head_list:
        occupation_groups.append({
            "cat_id": category.get("cat_id"),
            "cat_name": category.get("cat_name"),
            "occupations": []
        })

    # ---------------------------------------
    # Put occupations under their category
    # ---------------------------------------
    for occupation in occupation_list:
        occupation_category = occupation.get( "occupation_category" )
        for category in occupation_groups:

            # If occupation_category contains cat_id
            if str(occupation_category) == str(
                category.get("cat_id")
            ):
                category["occupations"].append(
                    occupation
                )

                break

    return occupation_groups
    
def get_raasi_list(request):
    payload, headers = common_payload(request)
    raasi_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/socioReligious/raasi",
        json = payload,
        headers = headers,
        timeout = 10
    )
    raasis = raasi_response.json()
    return raasis

def get_star_list(request):
    payload, headers = common_payload(request)
    star_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/socioReligious/star",
        json = payload,
        headers = headers,
        timeout = 10
    )
    stars = star_response.json()
    return stars

def get_county_list(request):
    payload, headers = common_payload(request)
    country_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/location/country",
        json = payload,
        headers = headers,
        timeout = 10
    )
    countries = country_response.json()
    return countries

def get_indianState_list(request):
    payload, headers = common_payload(request)
    indianState_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/location/indianStates",
        json = payload,
        headers = headers,
        timeout = 10
    )
    indianStates = indianState_response.json()
    return indianStates 

def get_teluguCities_list(request):
    payload, headers = common_payload(request)
    teluguCities_response = requests.post(
        f"{settings.FASTAPI_BASE_URL}/location/telugCities",
        json = payload,
        headers = headers,
        timeout = 10
    )
    telugCities = teluguCities_response.json()
    return telugCities 

def get_employees_data(request):
    db= SessionLocal()
    try:
        employees = (
            db.query(EnLogin)
            .order_by(EnLogin.login_id.desc())
            .all()
        )
        
        return employees
    except Exception as e:
        print("Employees Error:", e)
        return []

    finally:
        db.close()

def occupations_as_working(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": False,
                "message": "Only POST method allowed"
            },
            status=405
        )

    # --------------------------------
    # Authentication
    # --------------------------------
    payload, headers = common_payload(request)

    if payload is None or headers is None:
        return JsonResponse(
            {
                "status": False,
                "message": "Authentication required"
            },
            status=401
        )
        
    try:
        # --------------------------------
        # Get JavaScript data
        # --------------------------------
        data = json.loads(request.body)
        employee_status_id = data.get( "employee_status_id" )

        # --------------------------------
        # Only Working
        # --------------------------------
        if employee_status_id != "working":
            return JsonResponse({
                "status": False,
                "message": "Employee is not working",
                "data": []
            })

        # ==================================================
        # 1. Get Occupation Master Head
        # ==================================================
        occupation_head_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employmentDetails/occupationMasterHead",
            json=payload,
            headers=headers,
            timeout=10
        )

        # --------------------------------
        # Check authentication
        # --------------------------------
        if occupation_head_response.status_code == 401:
            request.session.flush()
            return JsonResponse(
                {
                    "status": False,
                    "message": "Session expired"
                },
                status=401
            )

        # --------------------------------
        # Get head data
        # --------------------------------
        occupation_head_data = ( occupation_head_response.json() )
        occupation_master_head_list = ( occupation_head_data.get( "data", [] ) )

        # ==================================================
        # 2. Get Occupations / Sub List
        # ==================================================
        occupation_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employmentDetails/occupations",
            json=payload,
            headers=headers,
            timeout=10
        )

        # --------------------------------
        # Check authentication
        # --------------------------------
        if occupation_response.status_code == 401:
            request.session.flush()
            return JsonResponse(
                {
                    "status": False,
                    "message": "Session expired"
                },
                status=401
            )

        # --------------------------------
        # Get occupation data
        # --------------------------------
        occupation_data = ( occupation_response.json() )
        occupation_list = ( occupation_data.get( "data", [] ) )

        # ==================================================
        # 3. Combine Head + Sub List
        # ==================================================
        occupation_groups = get_occupation_groups( occupation_master_head_list, occupation_list )

        # ==================================================
        # 4. Return Combined Data
        # ==================================================
        return JsonResponse({
            "status": True,
            "message": "Occupation groups fetched successfully",
            "data": occupation_groups
        })

    except requests.RequestException as e:
        print( "FastAPI connection error:", e )
        return JsonResponse(
            {
                "status": False,
                "message": "Unable to connect to FastAPI"
            },
            status=500
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": False,
                "message": "Invalid JSON request"
            },
            status=400
        )

def occupations_as_not_working(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": False,
                "message": "Only POST method allowed"
            },
            status=405
        )

    payload, headers = common_payload(request)

    if payload is None or headers is None:
        return JsonResponse(
            {
                "status": False,
                "message": "Authentication required"
            },
            status=401
        )

    try:
        data = json.loads(request.body)
        employee_status_id = data.get("employee_status_id")

        # ==========================================
        # Only NOT WORKING
        # ==========================================
        if employee_status_id != "notworking":
            return JsonResponse({
                "status": False,
                "message": "Invalid employment status",
                "data": []
            })

        # ==========================================
        # Get ONLY Not Working Occupations
        # ==========================================
        occupation_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employmentDetails/occupationsAsNotWorking",
            json=payload,
            headers=headers,
            timeout=10
        )

        if occupation_response.status_code == 401:
            request.session.flush()
            return JsonResponse(
                {
                    "status": False,
                    "message": "Session expired"
                },
                status=401
            )

        occupation_data = occupation_response.json()
        occupation_groups = occupation_data.get(
            "data",
            []
        )

        # ==========================================
        # Return
        # ==========================================
        return JsonResponse({
            "status": True,
            "message": "Not working occupations fetched successfully",
            "data": occupation_groups
        })

    except requests.RequestException as e:
        print( "FastAPI connection error:", e )
        return JsonResponse(
            {
                "status": False,
                "message": "Unable to connect to FastAPI"
            },
            status=500
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": False,
                "message": "Invalid JSON request"
            },
            status=400
        )

def get_liveEvents_list(request):
    db= SessionLocal()
    try:
        pv_events = (
            db.query(EnParichayaVedika)
            .order_by(EnParichayaVedika.id.desc())
            .all()
        )
        
        return pv_events
    except Exception as e:
        print("Events Error:", e)
        return []

    finally:
        db.close()

def get_banners_list(request):
    db = SessionLocal()
    try:
        banners = (
            db.query(EnBanners)
            .filter(
                # EnBanners.status == 1,
                # EnBanners.deleted == 0
            )
            .order_by(EnBanners.id.desc())
            .all()
        )
        return banners

    except Exception as e:
        print("Banner Error:", e)
        return []

    finally:
        db.close()

def get_package_categories_list():
    db = SessionLocal()

    try:
        packageCategories_list = (
            db.query(EnPackageCategories)
            .order_by(EnPackageCategories.id.desc())
            .all()
        )
        return packageCategories_list

    except Exception as e:
        print("Package Categories Error:", e)
        return []

    finally:
        db.close()

def get_package_subCategories_list():
    db = SessionLocal()

    try:
        packageSubCategories_list = (
            db.query(EnPackageSubcategories)
            .order_by(EnPackageSubcategories.cid.desc())
            .all()
        )

        return packageSubCategories_list

    except Exception as e:
        print("Package Subcategories Error:", e)
        return []

    finally:
        db.close()

def login_view(request):
    logout_success = request.session.pop("logout_success", False)

    # Already logged in
    if request.session.get("access_token"):
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            return render(request, "admin_app/login.html", {
                "error": "Please enter username and password."
            })

        db = SessionLocal()

        try:
            # ----------------------------------
            # 1. Get user from MySQL
            # ----------------------------------
            employee = db.query(EnLogin).filter( EnLogin.username == username ).first()

            if not employee:
                return render(request, "admin_app/login.html", {
                    "error": "Invalid username or password."
                })

            # ----------------------------------
            # 2. Verify password (MD5)
            # ----------------------------------
            entered_password = hashlib.md5( password.encode("utf-8") ).hexdigest()

            if employee.password != entered_password:
                return render(request, "admin_app/login.html", {
                    "error": "Invalid username or password."
                })

            # ----------------------------------
            # 3. Check employee status
            # ----------------------------------
            if employee.status != 1:
                return render(request, "admin_app/login.html", {
                    "error": "Your account is inactive."
                })

            # ----------------------------------
            # 4. Generate JWT Token
            # ----------------------------------
            token_data = {
                "sub": str(employee.login_id),
                "login_id": employee.login_id,
                "username": employee.username
            }

            access_token = create_access_token(token_data)

            # ----------------------------------
            # 5. Save Django Session
            # ----------------------------------
            request.session.cycle_key()
            request.session["access_token"] = access_token
            request.session["api_type"] = settings.FASTAPI_AUTH_TYPE
            request.session["api_authkey"] = settings.FASTAPI_AUTH_KEY
            request.session["user"] = {
                "login_id": employee.login_id,
                "username": employee.username
            }

            request.session["user_id"] = employee.login_id
            request.session["username"] = employee.username
            request.session.set_expiry(3600)
            return redirect("dashboard")

        except SQLAlchemyError as e:
            logging.exception("Database login error")
            return render(request, "admin_app/login.html", {
                "error": "Database connection error."
            })

        finally:
            db.close()

    return render(request, "admin_app/login.html", {
        "logout_success": logout_success
    })

@never_cache
def dashboard_view(request):
    if not request.session.get("user"):
        return redirect("login")

    # --------------------------------
    # Direct Database Queries
    # --------------------------------
    try:
        events_response = get_liveEvents_list(request)
        employees_response = get_employees_data(request)

        # Registrations Direct Database
        (
            registers_status_code,
            registers,
            total_registrations,
            male_registartions,
            female_registartions,
            today_registrations,
            this_month_registrations
        ) = get_registartions_data(request)

        total_employees = len(employees_response)
        total_events = len(events_response)

    except Exception as e:

        print("Dashboard Database Error:", e)

        return render(
            request,
            "admin_app/dashboard.html",
            {
                "error": "Unable to load dashboard data."
            }
        )

    # --------------------------------
    # Dashboard data
    # --------------------------------
    data = {
        "total_employees": total_employees,
        "total_events": total_events,
        "total_registrations": total_registrations,
        "male_registartions": male_registartions,
        "female_registartions": female_registartions,
        "user": request.session.get("user", {}),
        "template": "dashboard",
    }

    return render(
        request,
        "admin_app/dashboard.html",
        data
    )

def logout_view(request):

    # Clear Django session
    request.session.flush()

    # Logout success message
    messages.success(
        request,
        "You have been securely logged out."
    )

    return redirect("login")

@never_cache
def user_view(request):
    try:
        # --------------------------------
        # 1. Registration Data (SQLAlchemy)
        # --------------------------------
        (
            registers_status_code,
            registers_response,
            total_registrations,
            male_registartions,
            female_registartions,
            today_registrations,
            this_month_registrations
        ) = get_registartions_data(request)

        # --------------------------------
        # 2. JWT Session Check
        # --------------------------------
        if registers_status_code == 401:
            request.session.flush()
            return redirect("login")

        # --------------------------------
        # 3. Registration Error Check
        # --------------------------------
        if registers_status_code != 200:
            return render(
                request,
                "admin_app/users.html",
                {
                    "error": registers_response.get(
                        "message",
                        "Unable to load registrations."
                    )
                }
            )

        # Registration records
        register_users = registers_response.get("data", [])

        # --------------------------------
        # 4. Religion
        # --------------------------------
        religion_response = get_religion_list(request)

        if isinstance(religion_response, dict):
            religion_list = religion_response.get("data", [])
        else:
            religion_list = religion_response

        # --------------------------------
        # 5. Christian Denomination
        # --------------------------------
        christianDenomination_response = get_christianDenomination_list(request)

        if isinstance(christianDenomination_response, dict):
            christianDenomination_list = christianDenomination_response.get("data", [])
        else:
            christianDenomination_list = christianDenomination_response

        # --------------------------------
        # 6. Muslim Subsects
        # --------------------------------
        muslimSubsects_response = get_muslimSubsects_list(request)

        if isinstance(muslimSubsects_response, dict):
            muslimSubsects_list = muslimSubsects_response.get("data", [])
        else:
            muslimSubsects_list = muslimSubsects_response

        # --------------------------------
        # 7. Caste
        # --------------------------------
        caste_response = get_cste_list(request)

        if isinstance(caste_response, dict):
            caste_list = caste_response.get("data", [])
        else:
            caste_list = caste_response

        # --------------------------------
        # 8. Height
        # --------------------------------
        height_response = get_height_list(request)

        if isinstance(height_response, dict):
            height_list = height_response.get("data", [])
        else:
            height_list = height_response

        # --------------------------------
        # 9. Education Qualification
        # --------------------------------
        educationQualification_response = get_education_qualification_list(request)

        if isinstance(educationQualification_response, dict):
            educationQualification_list = educationQualification_response.get("data", [])
        else:
            educationQualification_list = educationQualification_response

        # --------------------------------
        # 10. Raasi
        # --------------------------------
        raasi_response = get_raasi_list(request)

        if isinstance(raasi_response, dict):
            raasi_list = raasi_response.get("data", [])
        else:
            raasi_list = raasi_response

        # --------------------------------
        # 11. Star
        # --------------------------------
        star_response = get_star_list(request)

        if isinstance(star_response, dict):
            star_list = star_response.get("data", [])
        else:
            star_list = star_response

        # --------------------------------
        # 12. Country
        # --------------------------------
        country_response = get_county_list(request)

        if isinstance(country_response, dict):
            counry_list = country_response.get("data", [])
        else:
            counry_list = country_response

        # --------------------------------
        # 13. Indian States
        # --------------------------------
        indianStates_response = get_indianState_list(request)

        if isinstance(indianStates_response, dict):
            inadian_states_list = indianStates_response.get("data", [])
        else:
            inadian_states_list = indianStates_response

        # --------------------------------
        # 14. Telugu Cities
        # --------------------------------
        teluguCities_response = get_teluguCities_list(request)

        if isinstance(teluguCities_response, dict):
            teluguCities_list = teluguCities_response.get("data", [])
        else:
            teluguCities_list = teluguCities_response

        # --------------------------------
        # 15. Occupation Master Head
        # --------------------------------
        occupationMasterHead_response = get_occupation_master_head_list(request)

        if isinstance(occupationMasterHead_response, dict):
            occupationMasterHead_list = occupationMasterHead_response.get("data", [])
        else:
            occupationMasterHead_list = occupationMasterHead_response

        # --------------------------------
        # 16. Occupation
        # --------------------------------
        occupation_response = get_occupation_list(request)

        if isinstance(occupation_response, dict):
            ocupation_list = occupation_response.get("data", [])
        else:
            ocupation_list = occupation_response

        # --------------------------------
        # 17. Occupation Groups
        # --------------------------------
        occupation_groups = get_occupation_groups(
            occupationMasterHead_list,
            ocupation_list
        )

        # --------------------------------
        # 18. Income
        # --------------------------------
        income_response = get_income_list(request)

        if isinstance(income_response, dict):
            income_list = income_response.get("data", [])
        else:
            income_list = income_response

        # --------------------------------
        # 19. Employees
        # --------------------------------
        employees_response = get_employees_data(request)

        if hasattr(employees_response, "json"):
            employee_response_data = employees_response.json()
            employee_list = employee_response_data.get("data", [])

        elif isinstance(employees_response, dict):
            employee_list = employees_response.get("data", [])

        else:
            employee_list = employees_response

    except requests.RequestException as e:

        print("FastAPI connection error:", e)

        return render(
            request,
            "admin_app/users.html",
            {
                "error": "Unable to connect to API server."
            }
        )

    except Exception as e:

        print("User View Error:", e)

        return render(
            request,
            "admin_app/users.html",
            {
                "error": str(e)
            }
        )

    # --------------------------------
    # 20. Send Data to Template
    # --------------------------------
    data = {

        "total_registrations": total_registrations,
        "male_registartions": male_registartions,
        "female_registartions": female_registartions,
        "today_registrations": today_registrations,
        "this_month_registrations": this_month_registrations,

        "register_users": register_users,

        "religion_list": religion_list,
        "christianDenomination_list": christianDenomination_list,
        "muslimSubsects_list": muslimSubsects_list,

        "caste_list": caste_list,
        "height_list": height_list,

        "educationQualification_list": educationQualification_list,

        "raasi_list": raasi_list,
        "star_list": star_list,

        "teluguCities_list": teluguCities_list,
        "counry_list": counry_list,
        "inadian_states_list": inadian_states_list,

        "occupation_groups": occupation_groups,

        "income_list": income_list,
        "employee_list": employee_list,

        "template": "users",
    }

    # --------------------------------
    # 21. Create User Result
    # --------------------------------
    create_user_result = request.session.pop(
        "create_user_result",
        None
    )

    data["create_user_result"] = create_user_result

    # --------------------------------
    # 22. Render Template
    # --------------------------------
    return render(
        request,
        "admin_app/users.html",
        data
    )

logger = logging.getLogger(__name__)
def form_value(data, key, default=""):
    return (data.get(key) or default).strip()

def get_int(data, key, default=None):
    value = form_value(data, key)

    if not value:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value for {key}")

def calculate_age(dob_date):
    today = date.today()
    age = today.year - dob_date.year
    if (today.month, today.day) < (dob_date.month, dob_date.day):
        age -= 1

    return age

def get_timestamp():
    return int(datetime.now().timestamp())

def createUser(request):
    # =========================================
    # GET: Dropdown data from FastAPI
    # =========================================
    if request.method == "GET":
        return user_view(request)

    # =========================================
    # Only POST allowed
    # =========================================
    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "message": "Only POST method is allowed"
        }, status=405)

    # =========================================
    # Django Session Authentication
    # =========================================
    if not request.session.get("access_token"):
        return redirect("login")

    db = SessionLocal()

    try:
        data = request.POST

        # =====================================
        # 1. Basic validations
        # =====================================
        name = form_value(data, "createName")
        gender = form_value(data, "gender")
        mobile = form_value(data, "phoneNumber")
        dob = form_value(data, "dob")

        if not name:
            raise ValueError("Name is required.")

        if gender not in ["M", "F"]:
            raise ValueError("Please select valid gender.")

        if len(mobile) != 10 or not mobile.isdigit():
            raise ValueError("Mobile number must contain 10 digits.")

        if not dob:
            raise ValueError("Date of birth is required.")

        dob_date = datetime.strptime(
            dob, "%Y-%m-%d"
        ).date()

        age = calculate_age(dob_date)

        if age < 18:
            raise ValueError("Age must be at least 18.")

        # EngRegister.dob is Integer.
        # Here we store Unix timestamp.
        dob_timestamp = int(
            datetime.combine(
                dob_date,
                datetime.min.time()
            ).timestamp()
        )

        # =====================================
        # 2. Religion and caste
        # =====================================
        religion_id = get_int(data, "religion")
        caste_id = get_int(data, "caste")

        if not religion_id or not caste_id:
            raise ValueError("Religion and caste are required.")

        denomination = get_int( data, "denomination", 0 )
        subcaste = form_value(data, "subcaste")

        # =====================================
        # 3. Marital information
        # =====================================
        marital_status = get_int( data, "maritalStatus" )

        if marital_status is None:
            raise ValueError("Marital status is required.")

        childstatus = form_value( data, "childstatus", "N" )

        # =====================================
        # 4. Current and permanent address
        # =====================================
        state_id = get_int(data, "currentState")

        if state_id is None:
            raise ValueError("Current state is required.")

        livingin = get_int( data, "currentCountry" ) 
        temp_country = get_int( data, "permanentCountry" ) 
        temp_state = form_value( data, "permanentState" ) 
        temp_city = form_value( data, "permanentTeluguCities_list" ) 
        temp_town = form_value( data, "permanentVillage" )
        current_city = form_value( data, "currentCity" ) 
        current_village = form_value( data, "currentVillage" )

        # =====================================
        # 5. Multiple selection preferences
        # =====================================
        preference_marital_status = ",".join( data.getlist("preference_marital_status[]") ) 
        preference_country = ",".join( data.getlist("preference_country[]") ) 
        preference_state = ",".join( data.getlist("preference_state[]") ) 
        preference_city = ",".join( data.getlist("preference_city[]") ) 
        preference_religion = ",".join( data.getlist("preference_religion[]") ) 
        preference_caste = ",".join( data.getlist("preference_caste[]") ) 
        preference_education = ",".join( data.getlist("preference_education[]") ) 
        preference_occupation = ",".join( data.getlist("preference_occupation[]") ) 
        preference_income = ",".join( data.getlist("preference_incomeId[]") )

        # =====================================
        # 6. Generate registration values
        # =====================================
        current_timestamp = get_timestamp()
        temporary_profile_id = ( "TEMP-" + uuid.uuid4().hex )

        # =====================================
        # 7. Create EngRegister object
        # =====================================

        register = EngRegister(

            # Basic information
            profile_id=temporary_profile_id,
            password="",
            name=name,
            dob=dob_timestamp,
            tob=form_value(data, "tob"),
            age=age,
            gender=gender,

            # Religion
            religion_id=religion_id,
            denomination=denomination,
            caste_id=caste_id,
            subcaste=subcaste,

            # Citizenship
            citizenship=1,
            livingin=livingin,

            # Marital information
            maritialstatus=marital_status,
            childstatus=childstatus,

            # Address
            state_id=state_id,
            state_other=None,
            temp_country=temp_country,
            temp_state=temp_state,
            temp_city=temp_city,
            temp_town=temp_town,
            residing_city=current_city,
            residing_other_city=current_village,

            # Photos and security
            hasphoto=0,
            hasvideo=0,
            photopassword="",
            isprotected=0,
            hasastro=0,

            # Registration dates
            datecreated=current_timestamp,
            valid_upto=current_timestamp,
            valid_upto_time="",
            grace_time="",
            date_deactivated=date.today(),

            # Registration status
            member_status=0,
            featured_member=0,
            isactive=0,
            status=1,
            deleted=0,

            # Login settings
            generated_password="",
            loginstatus=0,

            # Contact limits
            view_contacts_limit=getattr( settings, "REGISTER_VIEW_CONTACTS_LIMIT", 0 ),
            pm_limit=getattr( settings, "REGISTER_PM_LIMIT", 0 ),

            # Registration source
            register_from="WEB",
            offline_empid=form_value( data, "offline_empid" ),

            # Personal information
            privacy_access=0,

            # Preferences are not EngRegister columns.
            # They may belong to related tables.
        )

        # =====================================
        # 8. Direct MySQL INSERT
        # =====================================

        db.add(register)

        # INSERT execute చేసి auto increment ID పొందుతాం.
        db.flush()

        register_id = register.register_id

        # Generate final profile ID.
        register.profile_id = ( f"EP{register_id:06d}" )

        # Save everything permanently.
        db.commit()
        db.refresh(register)
        logger.info(
            "Registration inserted successfully. ID=%s",
            register_id
        )

        # =====================================
        # 9. Success message
        # =====================================
        request.session["create_user_result"] = {
            "success": True,
            "message": "Registration created successfully.",
            "register_id": register_id,
            "profile_id": register.profile_id
        }
        return redirect("createUser")

    # =========================================
    # Validation error
    # =========================================

    except ValueError as e:
        db.rollback()
        logger.warning(
            "Registration validation failed: %s",
            str(e)
        )

        request.session["create_user_result"] = {
            "success": False,
            "message": str(e)
        }
        return redirect("createUser")

    # =========================================
    # Database error
    # =========================================

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception( "Registration database insert failed" )
        request.session["create_user_result"] = {
            "success": False,
            "message": "Database insertion failed: " + str(e)
        }
        return redirect("createUser")

    # =========================================
    # Unexpected error
    # =========================================
    except Exception as e:
        db.rollback()
        logger.exception(
            "Unexpected registration error"
        )
        request.session["create_user_result"] = {
            "success": False,
            "message": str(e)
        }
        return redirect("createUser")

    finally:
        db.close()

@never_cache
def banners_view(request):
    if not request.session.get("user"):
        return redirect("login")

    banners_list = get_banners_list(request)
    return render(
        request,
        "admin_app/banners.html",
        {
            "banners_list": banners_list
        }
    )

@never_cache
def pacakges_view(request):

    if not request.session.get("user"):
        return redirect("login")

    packageCategories_list = get_package_categories_list()
    return render(
        request,
        "admin_app/packages.html",
        {
            "packageCategories_list": packageCategories_list
        }
    )
    data = {
        "packageCategories_list": packageCategories_list
    }
    return render(request, "admin_app/packages.html", data)

@never_cache
def subPacakges_view(request):

    if not request.session.get("user"):
        return redirect("login")

    packageSubCategories_list = get_package_subCategories_list()
    data = {
        "packageSubCategories_list": packageSubCategories_list
    }
    return render(request, "admin_app/subPackages.html", data)

@never_cache
def liveEvents_view(request):

    if not request.session.get("user"):
        return redirect("login")

    liveEvents_list = get_liveEvents_list(request)
    data = {
        "liveEvents_list": liveEvents_list
    }
    return render(request, "admin_app/liveEvents.html", data)
