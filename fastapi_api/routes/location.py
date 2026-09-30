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

@router.post("/indianStates")
def get_indianStates_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    indianStates = db.query(EnStateMaster).filter(EnStateMaster.country_id == 1).all()
    return {
        "status": True,
        "message": "States fetched successfully",
        "data": [
            {
                "state_id": ist.state_id,
                "state_name": ist.state_name,
                "country_id_old": ist.country_id_old,
                "country_id": ist.country_id,
                "status": ist.status,
                "deleted": ist.deleted,
            }
            for ist in indianStates
        ]
    }

@router.post("/telugCities")
def get_teluguCities_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")
    telugu_cities = db.query(EnCity).filter( EnCity.state_id.in_([2, 3193]) ).all()

    return {
        "status": True,
        "message": "States fetched successfully",
        "data": [
            {
                "city_id": tct.city_id,
                "city_name": tct.city_name,
                "state_id": tct.state_id,
                "country_id": tct.country_id,
                "status":tct.status,
            }
            for tct in telugu_cities
        ]
    }
