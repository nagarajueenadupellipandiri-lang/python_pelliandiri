from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnRaasiMaster, EnStarMaster, EnQualificationMaster)

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/educationDetails", tags=["Education Details"] )

@router.post("/raasi")
def get_qualification_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    qualification = db.query(EnQualificationMaster).all()
    return {
        "status": True,
        "message": "Stars fetched successfully",
        "data": [
            {
                "qualification_id": qual.qualification_id,
                "qualification": qual.qualification,
                "status": qual.status,
                "deleted": qual.deleted,
                "order_id": qual.order_id,
            }
            for qual in qualification
        ]
    }
