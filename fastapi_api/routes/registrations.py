from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from database import get_db
from models import EngRegister

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/registrations", tags=["Registrations"] )

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
    # 2. Read params
    # =========================================================
    params = request.params or {}

    # =========================================================
    # 3. Page
    # =========================================================
    try:
        page = int(params.get("page", 1))
    except (TypeError, ValueError):
        page = 1


    # =========================================================
    # 4. Limit
    # =========================================================
    try:
        limit = int(params.get("limit", 50))
    except (TypeError, ValueError):
        limit = 50


    # =========================================================
    # 5. Validate page
    # =========================================================
    if page < 1:
        page = 1


    # =========================================================
    # 6. Validate limit
    # =========================================================
    if limit < 1:
        limit = 50

    # Maximum 100 records per request
    if limit > 100:
        limit = 100


    # =========================================================
    # 7. Search
    # =========================================================
    search = params.get("search", "")

    if search is None:
        search = ""

    search = str(search).strip()


    # =========================================================
    # 8. Base query
    # =========================================================
    query = db.query(EngRegister)

    # =========================================================
    # 9. Apply search
    # =========================================================
    if search:
        search_value = f"%{search}%"
        query = query.filter(
            or_(
                EngRegister.profile_id.ilike(search_value),
                EngRegister.name.ilike(search_value)
            )
        )


    # =========================================================
    # 10. Total records
    # =========================================================
    total_registrations = query.with_entities(
        func.count(EngRegister.register_id)
    ).scalar()
    total_registrations = total_registrations or 0


    # =========================================================
    # 11. Calculate total pages
    # =========================================================
    total_pages = (
        (total_registrations + limit - 1) // limit
        if total_registrations > 0
        else 0
    )


    # =========================================================
    # 12. Calculate offset
    # =========================================================
    offset = (page - 1) * limit


    # =========================================================
    # 13. Get current page records
    # =========================================================
    registrations = (
        query
        .order_by(EngRegister.register_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


    # =========================================================
    # 14. Prepare response data
    # =========================================================
    data = []
    for reg in registrations:
        data.append({
            "register_id": reg.register_id,
            "profile_id": reg.profile_id,
            "name": reg.name,
            "dob": reg.dob,
            "tob": reg.tob,
        })


    # =========================================================
    # 15. Final response
    # =========================================================
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