from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import EnHeightMaster

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/height", tags=["Height"] )

@router.post("")
def get_religion_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    heights = db.query(EnHeightMaster).all()
    return {
        "status": True,
        "message": "Heights fetched successfully",
        "data": [
            {
                "height_id": heig.height_id,
                "height": heig.height,
                "status": heig.status,
                "deleted": heig.deleted,
            }
            for heig in heights
        ]
    }
