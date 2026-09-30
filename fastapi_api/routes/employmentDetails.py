from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnOccupationMasterHead, EnOccupationMaster, EnIncomeMaster)

from core.security import ( validate_common_request, get_current_user, )

from schemas.common import CommonRequest

router = APIRouter( prefix="/employmentDetails", tags=["Employment-Details"] )

@router.post("/occupationMasterHead")
def get_occupationMasterHead_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")
    ocupationMaster = db.query(EnOccupationMasterHead).all()
    return {
        "status": True,
        "message": "EnOccupationMasterHead fetched successfully",
        "data": [
            {
                "cat_id": occu_mast.cat_id,
                "cat_name": occu_mast.cat_name,
            }
            for occu_mast in ocupationMaster
        ]
    }

@router.post("/occupations")
def get_occupation_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")

    occupations = (
        db.query(EnOccupationMaster)
        .filter(EnOccupationMaster.deleted == 0)
        .order_by(
            EnOccupationMaster.occupation_category,
            EnOccupationMaster.occupation
        )
        .all()
    )

    return {
        "status": True,
        "message": "Occupations fetched successfully",
        "data": [
            {
                "occupation_id": occupation.occupation_id,
                "occupation": occupation.occupation,
                "occupation_category": occupation.occupation_category,
                "status": occupation.status,
                "deleted": occupation.deleted,
            }
            for occupation in occupations
        ]
    }

@router.post("/occupationsAsNotWorking")
def get_occupation_list_notWorking(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")

    # --------------------------------
    # ONLY 2 occupation records
    # --------------------------------
    occupations = (
        db.query(EnOccupationMaster)
        .filter(
            EnOccupationMaster.deleted == 0,
            EnOccupationMaster.occupation_id.in_([1, 87])
        )
        .order_by( EnOccupationMaster.occupation_id )
        .all()
    )

    # --------------------------------
    # ONLY ONE HEADER
    # --------------------------------
    category = (
        db.query(EnOccupationMasterHead)
        .filter( EnOccupationMasterHead.cat_id == 10 )
        .first()
    )

    # --------------------------------
    # ONE HEADER + TWO ITEMS
    # --------------------------------
    return {
        "status": True,
        "message": "Not working occupations fetched successfully",
        "data": [
            {
                "cat_id": 10,
                "cat_name": (
                    category.cat_name
                    if category
                    else "Non working"
                ),
                "occupations": [
                    {
                        "occupation_id": occupation.occupation_id,
                        "occupation": occupation.occupation,
                        "occupation_category": occupation.occupation_category,
                        "status": occupation.status,
                        "deleted": occupation.deleted,
                    }
                    for occupation in occupations
                ]
            }
        ]
    }

@router.post("/incomes")
def get_incomeList_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")
    incomeMaster = db.query(EnIncomeMaster).all()
    return {
        "status": True,
        "message": "Income fetched successfully",
        "data": [
            {
                "income_id": income_mast.income_id,
                "income": income_mast.income,
                "currency_id": income_mast.currency_id,
                "status": income_mast.status,
                "deleted": income_mast.deleted,
            }
            for income_mast in incomeMaster
        ]
    }
