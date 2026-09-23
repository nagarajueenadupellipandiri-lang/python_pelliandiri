import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

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

def get_employees_data(request):
    payload, headers = common_payload(request)

    employees_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employees",
            json=payload,
            headers=headers,
            timeout=10
        )
    return employees_response

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

        print("=========registers data:========", registers)
        print("=========total registrations:=========", total_registrations)

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

# def user_view(request):

#     payload, headers = common_payload(request)

#     if payload is None or headers is None:
#         return redirect("login")

#     # --------------------------------
#     # Call FastAPI APIs
#     # --------------------------------
#     try:
#         (registers_status_code, registers, total_registrations) = get_registartions_data(request)

#         print("=========registers data:========", registers)
#         print("=========total registrations:=========", total_registrations)

#     except requests.RequestException as e:
#         print("FastAPI connection error:", e)

#         return render(
#             request,
#             "admin_app/dashboard.html",
#             {
#                 "error": "Unable to connect to API server."
#             }
#         )
    
#     data = {
#         "total_registrations": total_registrations,
#         "registers": registers,
#     }
        
#     return render( request, "admin_app/users.html", data)

def user_view(request):

    payload, headers = common_payload(request)

    if payload is None or headers is None:
        return redirect("login")

    # --------------------------------
    # Call FastAPI API
    # --------------------------------
    try:

        (
            registers_status_code,
            registers_response,
            total_registrations
        ) = get_registartions_data(request)

        print(
            "========= registers response: =========",
            registers_response
        )

        print(
            "========= total registrations: =========",
            total_registrations
        )

        # Get only registration data
        # registers = registers_response.get("data", [])
        register_users = registers_response.get("data", [])

        print(
            "========= registration list: =========",
            register_users
        )

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
        # "registers": registers,
        "register_users": register_users,
    }

    return render(
        request,
        "admin_app/users.html",
        data
    )

