from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import EnLogin

from core.security import (
    validate_common_request,
    get_current_user,
    create_access_token
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/employees", tags=["Employees"] )

@router.post("")
def get_employees(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    employee = db.query(EnLogin).all()
    total_employees = len(employee)
    return {
        "status": True,
        "message": "Employees fetched successfully",
        "total_employees": total_employees,
        "data": [
            {
                "login_id": emp.login_id,
                "emp_id": emp.emp_id,
                "username": emp.username,
                "emp_email": emp.emp_email,
                "status": emp.status,
                "dept_id": emp.dept_id,
                "is_super_admin": emp.is_super_admin
            }
            for emp in employee
        ]
    }


