from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnRaasiMaster, EnStarMaster)

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/socioReligious", tags=["Socio-Religious"] )

@router.post("/raasi")
def get_raasi_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    raasis = db.query(EnRaasiMaster).all()
    return {
        "status": True,
        "message": "Stars fetched successfully",
        "data": [
            {
                "raasi_id": rs.raasi_id,
                "raasi": rs.raasi,
                "status": rs.status,
                "deleted": rs.deleted,
            }
            for rs in raasis
        ]
    }


@router.post("/star")
def get_star_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    stars = db.query(EnStarMaster).all()
    return {
        "status": True,
        "message": "Religion fetched successfully",
        "data": [
            {
                "star_id": st.star_id,
                "star": st.star,
                "status": st.status,
                "deleted": st.deleted,
            }
            for st in stars
        ]
    }

