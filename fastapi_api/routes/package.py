from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import(EnPackageCategories)

from core.security import ( validate_common_request, get_current_user, )
from schemas.common import CommonRequest

router = APIRouter( prefix="/packages", tags=["packageInfo"] )

@router.post("/categories")
def get_category_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")
    ctegory = (
        db.query(EnPackageCategories)
        # .filter(EnReligionMaster.religion_id.in_([1, 2, 3, 20]))
        # .order_by(EnReligionMaster.religion_id.asc())
        .all()
    )

    return {
        "status": True,
        "message": "Religion fetched successfully",
        "data": [
            {
                "id": cat.id,
                "package_name": cat.package_name,
                "status": cat.status,
                "datecreated": cat.datecreated,
            }
            for cat in ctegory
        ]
    }

