from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnCountryMaster, EnStateMaster, EnCity)

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/location", tags=["Location"] )

@router.post("/country")
def get_country_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    countries = db.query(EnCountryMaster).all()
    return {
        "status": True,
        "message": "Countries fetched successfully",
        "data": [
            {
                "country_id": cnt.country_id,
                "isd_code": cnt.isd_code,
                "country_name": cnt.country_name,
                "status": cnt.status,
                "deleted": cnt.deleted,
            }
            for cnt in countries
        ]
    }

@router.post("/state")
def get_state_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    states = db.query(EnStateMaster).all()
    return {
        "status": True,
        "message": "States fetched successfully",
        "data": [
            {
                "state_id": st.state_id,
                "state_name": st.state_name,
                "country_id_old": st.country_id_old,
                "country_id": st.country_id,
                "status":st.status,
                "deleted": st.deleted,
            }
            for st in states
        ]
    }

@router.post("/city")
def get_city_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    cities = db.query(EnCity).all()
    return {
        "status": True,
        "message": "States fetched successfully",
        "data": [
            {
                "city_id": ct.city_id,
                "city_name": ct.city_name,
                "state_id": ct.state_id,
                "country_id": ct.country_id,
                "status":ct.status,
            }
            for ct in cities
        ]
    }
