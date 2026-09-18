from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import EngRegister

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest


router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)


@router.post("")
def get_registrations(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # =========================================================
    # 1. Validate common request
    # =========================================================
    validate_common_request(request, "login")


    # =========================================================
    # 2. Read pagination from params
    # =========================================================
    params = request.params or {}

    try:
        page = int(params.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    try:
        limit = int(params.get("limit", 20))
    except (TypeError, ValueError):
        limit = 20


    # =========================================================
    # 3. Validate page and limit
    # =========================================================
    if page < 1:
        page = 1

    if limit < 1:
        limit = 20

    # Maximum 100 records per request
    if limit > 100:
        limit = 100


    # =========================================================
    # 4. Calculate offset
    # =========================================================
    offset = (page - 1) * limit


    # =========================================================
    # 5. Get total count
    # =========================================================
    total_registrations = (
        db.query(func.count(EngRegister.register_id))
        .scalar()
    )

    total_registrations = total_registrations or 0

    # =========================================================
    # 6. Get only required records
    # =========================================================
    registrations = (
        db.query(EngRegister)
        .offset(offset)
        .limit(limit)
        .all()
    )


    # =========================================================
    # 7. Prepare response
    # =========================================================
    data = []

    for reg in registrations:
        data.append({
            "register_id": reg.register_id,
            "profile_id": reg.profile_id,
            "name": reg.name,
            "dob": reg.dob,
            "tob": reg.tob
        })


    # =========================================================
    # 8. Pagination information
    # =========================================================
    total_pages = (
        (total_registrations + limit - 1) // limit
        if total_registrations > 0
        else 0
    )


    # =========================================================
    # 9. Final response
    # =========================================================
    return {
        "status": True,
        "message": "Registrations fetched successfully",

        "pagination": {
            "page": page,
            "limit": limit,
            "total_registrations": total_registrations,
            "total_pages": total_pages
        },

        "data": data
    }