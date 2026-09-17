import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

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

# ----------------------------------------
# Dashboard
# ----------------------------------------
def dashboard_view(request):

    # --------------------------------
    # Get JWT from Django session
    # --------------------------------
    access_token = request.session.get("access_token")

    # JWT not available
    if not access_token:
        return redirect("login")

    api_type = request.session.get("api_type")
    api_authkey = request.session.get("api_authkey")

    # --------------------------------
    # API configuration not available
    # --------------------------------
    if not api_type or not api_authkey:
        request.session.flush()
        return redirect("login")

    # --------------------------------
    # Common API payload
    # --------------------------------
    common_payload = {
        "type": api_type,
        "Authkey": api_authkey,
        "params": {}
    }

    # --------------------------------
    # JWT Authorization
    # --------------------------------
    headers = { "Authorization": f"Bearer {access_token}" }

    # --------------------------------
    # Call FastAPI Employees API
    # --------------------------------
    try:
        employees_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/employees",
            json=common_payload,
            headers=headers,
            timeout=10
        )
        
        events_response = requests.post(
            f"{settings.FASTAPI_BASE_URL}/parichayaVedika",
            json=common_payload,
            headers=headers,
            timeout=10
        )

        employees = employees_response.json()
        events = events_response.json()

    except requests.RequestException as e:
        print("FastAPI connection error:", e)
        return render(
            request,
            "admin_app/dashboard.html", { "error": "Unable to connect to API server." }
        )

    # --------------------------------
    # JWT invalid / expired
    # --------------------------------
    if employees_response.status_code == 401:
        request.session.flush()
        return redirect("login")

    # --------------------------------
    # API error
    # --------------------------------
    if ( employees_response.status_code != 200 or not employees.get("status") ):
        return render(
            request,
            "admin_app/dashboard.html",
            {
                "error": employees.get( "message", "Unable to load employees." )
            }
        )

    # --------------------------------
    # Get employee count
    # --------------------------------
    total_employees = employees.get( "total_employees", 0 )
    total_events = events.get("total_events", 0)

    # --------------------------------
    # Dashboard data
    # --------------------------------
    data = {
        "total_employees": total_employees,
        "total_events": total_events,
        "user": request.session.get( "user", {} )
    }

    # --------------------------------
    # Render dashboard
    # --------------------------------
    print("dta is ", data)
    return render( request, "admin_app/dashboard.html", data )

# ----------------------------------------
# Logout
# ----------------------------------------
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
