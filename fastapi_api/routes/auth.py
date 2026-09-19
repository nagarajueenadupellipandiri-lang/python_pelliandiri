import hashlib
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import EnLogin
from schemas.auth import LoginRequest, LogoutRequest

from core.security import ( 
    create_access_token, 
    validate_common_request,
    get_current_user
)

router = APIRouter( prefix="/auth", tags=["Authentication"] )

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    employee = db.query(EnLogin).filter(
        EnLogin.username == request.params.username
    ).first()

    if not employee:
        return {
            "status": False,
            "message": "Invalid username"
        }

    password_md5 = hashlib.md5(
        request.params.password.encode("utf-8")
    ).hexdigest()

    if employee.password != password_md5:
        return {
            "status": False,
            "message": "Invalid password"
        }

    if employee.status != 1:
        return {
            "status": False,
            "message": "Employee account is inactive"
        }

    access_token = create_access_token({
        "login_id": employee.login_id,
        "username": employee.username,
        "is_super_admin": employee.is_super_admin
    })

    return {
        "status": True,
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",

         # API configuration
        "api": {
            "type": request.type,
            "Authkey": request.Authkey
        },

        "data": {
            "login_id": employee.login_id,
            "emp_id": employee.emp_id,
            "username": employee.username,
            "emp_email": employee.emp_email,
            "user_level": employee.user_level,
            "dept_id": employee.dept_id,
            "is_super_admin": employee.is_super_admin
        }
    }


@router.post("/logout")
def logout(
    request: LogoutRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "logout")

    return {
        "status": True,
        "message": "Logout successful",
        "data": {
            "login_id": current_user.get("login_id"),
            "username": current_user.get("username")
        }
    }
