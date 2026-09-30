import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import json
from django.http import JsonResponse
from django.conf import settings

def common_payload(request):
    access_token = request.session.get("access_token")

    if not access_token:
        return redirect("login")

    api_type = request.session.get("api_type")
    api_authkey = request.session.get("api_authkey")

    if not api_type or not api_authkey:
        request.session.flush()
        return redirect("login")

    payload = { "type": api_type, "Authkey": api_authkey, "params": {} }
    headers = { "Authorization": f"Bearer {access_token}" }

    return payload, headers

def get_registartions_data(request):
    payload, headers = common_payload(request)

    registers_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/registrations/getRegistartions",
            json=payload,
            headers=headers,
            timeout=10
        )

    registers = registers_response.json()
    total_registrations = registers.get( "pagination", {} ) .get( "total_registrations", 0 )

    return (
        registers_response.status_code, 
        registers, 
        total_registrations
    )

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

# ============================
# def get_state_list(request):
#     payload, headers = common_payload(request)
#     country_response = requests.post(
#         f"{settings.FASTAPI_BASE_URL}/location/state",
#         json = payload,
#         headers = headers,
#         timeout = 10
#     )
#     states = country_response.json()
#     return states
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
# ============================
def get_employees_data(request):
    payload, headers = common_payload(request)

    employees_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employees",
            json=payload,
            headers=headers,
            timeout=10
        )
    return employees_response

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

def get_events_data(request):
    payload, headers = common_payload(request)
    
    events_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/parichayaVedika",
            json=payload,
            headers=headers,
            timeout=10
        )
    return events_response

def login_view(request):

    logout_success = request.session.pop(
        "logout_success",
        False
    )

    if request.method == "POST":

        username = request.POST.get( "username", "" ).strip()
        password = request.POST.get( "password", "" )

        payload = {
            "type": settings.FASTAPI_AUTH_TYPE,
            "Authkey": settings.FASTAPI_AUTH_KEY,
            "params": {
                "username": username,
                "password": password
            }
        }

        try:

            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/login",
                json=payload,
                timeout=10
            )

            data = response.json()

        except requests.RequestException:

            return render(
                request,
                "admin_app/login.html",
                {
                    "error": "FastAPI server is not available."
                }
            )

        except ValueError:

            return render(
                request,
                "admin_app/login.html",
                {
                    "error": "Invalid response from FastAPI."
                }
            )

        # --------------------------------------
        # Login failed
        # --------------------------------------
        if response.status_code != 200:

            return render(
                request,
                "admin_app/login.html",
                {
                    "error": data.get(
                        "message",
                        data.get(
                            "detail",
                            "Invalid username or password."
                        )
                    )
                }
            )

        if not data.get("status"):

            return render(
                request,
                "admin_app/login.html",
                {
                    "error": data.get(
                        "message",
                        "Login failed."
                    )
                }
            )

        # --------------------------------------
        # Login success
        # --------------------------------------

        access_token = data.get( "access_token" )
        user = data.get( "data", {} )
        if not access_token:

            return render(
                request,
                "admin_app/login.html",
                {
                    "error": "Access token not received."
                }
            )

        # --------------------------------------
        # API configuration
        # --------------------------------------

        api_type = settings.FASTAPI_AUTH_TYPE
        api_authkey = settings.FASTAPI_AUTH_KEY

        # --------------------------------------
        # Save session
        # --------------------------------------

        request.session["access_token"] = access_token
        request.session["api_type"] = api_type
        request.session["api_authkey"] = api_authkey
        request.session["user"] = user

        request.session["user_id"] = user.get(
            "login_id"
        )

        request.session["username"] = user.get(
            "username"
        )

        request.session.modified = True

        return redirect("dashboard")

    # --------------------------------------
    # Login page
    # --------------------------------------

    return render(
        request,
        "admin_app/login.html",
        {
            "logout_success": logout_success
        }
    )

def dashboard_view(request):
    payload, headers = common_payload(request)

    if payload is None or headers is None:
        return redirect("login")

    # --------------------------------
    # Call FastAPI APIs
    # --------------------------------
    try:
        events_response = get_events_data(request)
        employees_response = get_employees_data(request)
        registers_status_code, registers, total_registrations = get_registartions_data(request)
        employees = employees_response.json()
        events = events_response.json()

    except requests.RequestException as e:
        print("FastAPI connection error:", e)

        return render(
            request,
            "admin_app/dashboard.html",
            {
                "error": "Unable to connect to API server."
            }
        )

    # --------------------------------
    # JWT invalid / expired
    # --------------------------------
    if (
        employees_response.status_code == 401
        or events_response.status_code == 401
        or registers_status_code == 401
    ):
        request.session.flush()
        return redirect("login")

    # --------------------------------
    # Employees API error
    # --------------------------------
    if (
        employees_response.status_code != 200
        or not employees.get("status")
    ):
        return render(
            request,
            "admin_app/dashboard.html",
            {
                "error": employees.get(
                    "message",
                    "Unable to load employees."
                )
            }
        )

    # --------------------------------
    # Dashboard totals
    # --------------------------------
    total_employees = employees.get( "total_employees", 0 )
    total_events = events.get( "total_events", 0 )

    # --------------------------------
    # Dashboard data
    # --------------------------------
    data = {
        "total_employees": total_employees,
        "total_events": total_events,
        "total_registrations": total_registrations,
        "user": request.session.get( "user", {} ),
    }

    return render( request, "admin_app/dashboard.html", data )

def logout_view(request):
    access_token = request.session.get("access_token")
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "type": "logout",
            "Authkey": settings.FASTAPI_AUTH_KEY,
            "params": {}
        }

        try:
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/logout",
                json=payload,
                headers=headers,
                timeout=10
            )
            print("LOGOUT STATUS:", response.status_code)

        except requests.RequestException as e:
            print("FASTAPI LOGOUT ERROR:", e)

    # Clear Django session
    request.session.flush()

    # Logout message
    messages.success(
        request,
        "You have been securely logged out."
    )

    return redirect("login")

def user_view(request):
    payload, headers = common_payload(request)

    if payload is None or headers is None:
        return redirect("login")

    # --------------------------------
    # Call FastAPI API
    # --------------------------------
    try:
        ( registers_status_code, registers_response, total_registrations ) = get_registartions_data(request)
        register_users = registers_response.get("data", [])

        religion_response = get_religion_list(request)
        religion_list = religion_response.get("data", [])

        christianDenomination_response  = get_christianDenomination_list(request)
        christianDenomination_list = christianDenomination_response.get("data", [])

        muslimSubsects_response = get_muslimSubsects_list(request)
        muslimSubsects_list = muslimSubsects_response.get("data", [])

        caste_response = get_cste_list(request)
        caste_list = caste_response.get("data", [])

        height_response = get_height_list(request)
        height_list = height_response.get("data", [])

        educationQualification_rsponse = get_education_qualification_list(request)
        educationQualification_list = educationQualification_rsponse.get("data", [])

        raasi_response = get_raasi_list(request)
        raasi_list = raasi_response.get("data", [])

        star_response = get_star_list(request)
        star_list = star_response.get("data", [])

        country_response = get_county_list(request)
        counry_list = country_response.get("data", [])

        indianStates_response = get_indianState_list(request)
        inadian_states_list = indianStates_response.get("data", [])
        print("type is ", inadian_states_list)

        occupationMasterHead_response = get_occupation_master_head_list(request)
        occupationMasterHead_list = occupationMasterHead_response.get("data", [])

        occupation_response = get_occupation_list(request)
        ocupation_list = occupation_response.get("data", [])

        occupation_groups = get_occupation_groups( occupationMasterHead_list, ocupation_list )

        income_response = get_income_list(request)
        income_list = income_response.get("data", [])

        employees_response = get_employees_data(request)
        employee_response_data= employees_response.json()
        employee_list = employee_response_data.get("data", [])

    except requests.RequestException as e:
        print("FastAPI connection error:", e)
        return render(
            request,
            "admin_app/users.html",
            {
                "error": "Unable to connect to API server."
            }
        )

    # --------------------------------
    # JWT invalid / expired
    # --------------------------------
    if registers_status_code == 401:
        request.session.flush()
        return redirect("login")

    # --------------------------------
    # API error
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

    # --------------------------------
    # Send data to template
    # --------------------------------
    data = {
        "total_registrations": total_registrations,
        "register_users": register_users,
        "religion_list": religion_list,
        "christianDenomination_list": christianDenomination_list,
        "muslimSubsects_list": muslimSubsects_list,
        "caste_list": caste_list,
        "height_list": height_list,
        "educationQualification_list": educationQualification_list,
        "raasi_list": raasi_list,
        "star_list": star_list,
        "counry_list": counry_list,
        "inadian_states_list": inadian_states_list,
        "occupation_groups": occupation_groups,
        "income_list": income_list,
        "employee_list": employee_list,
    }

    return render( request, "admin_app/users.html", data )

