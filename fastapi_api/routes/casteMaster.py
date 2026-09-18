from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import EnCasteMaster

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/caste", tags=["Caste"] )

@router.post("")
def get_caste_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    castes = db.query(EnCasteMaster).all()
    return {
        "status": True,
        "message": "Castes fetched successfully",
        "data": [
            {
                "caste_id": cst.caste_id,
                "caste_name": cst.caste_name,
                "religion_id": cst.religion_id,
                "status": cst.status,
                "deleted": cst.deleted,
            }
            for cst in castes
        ]
    }
