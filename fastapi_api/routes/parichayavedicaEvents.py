from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.parichayavedicaEvents import parichayavedicaEvents

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest


router = APIRouter(
    prefix="/parichayaVedika",
    tags=["ParichayaVedika"]
)


@router.post("")
def get_parichayavedicaEvents(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")

    events = db.query(parichayavedicaEvents).all()

    return {
        "status": True,
        "message": "Events fetched successfully",
        "total_events": len(events),
        "data": [
            {
                "id": event.id,
                "eng_title": event.eng_title,
            }
            for event in events
        ]
    }
