from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnCasteMaster, EnReligionMaster, EnHeightMaster)

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/basiInfo", tags=["Basic Info"] )

@router.post("/religion")
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


@router.post("/caste")
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

@router.post("/height")
def get_height_list(
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
