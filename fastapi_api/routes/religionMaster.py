from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import EnReligionMaster

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/religion", tags=["Religion"] )

@router.post("")
def get_religion_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    religions = db.query(EnReligionMaster).all()
    return {
        "status": True,
        "message": "Religion fetched successfully",
        "data": [
            {
                "religion_id": rl.religion_id,
                "religion_name": rl.religion_name,
                "status": rl.status,
                "deleted": rl.deleted,
            }
            for rl in religions
        ]
    }
