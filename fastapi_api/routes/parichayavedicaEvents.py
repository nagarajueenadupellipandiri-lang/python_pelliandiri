from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import EnParichayaVedika

from core.security import (
    validate_common_request,
    get_current_user,
)

from schemas.common import CommonRequest

router = APIRouter( prefix="/parichayaVedika", tags=["ParichayaVedika"] )
@router.post("/parichayavedicaEvents")
def get_parichayavedica_events(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    validate_common_request(request, "login")

    events = db.query(EnParichayaVedika).all()

    return {
        "status": True,
        "message": "Events fetched successfully",
        "total_events": len(events),
        "data": [
            {
                "id": event.id,
                "eng_title": event.eng_title,
                "caste_id": event.caste_id,
                "address": event.address,
                "venue_address": event.venue_address,
                "online_link": event.online_link,
                "description": event.description,
                "start_date": event.id,
                "end_date": event.end_date,
                "display_date": event.display_date,
                "display_time": event.display_time,
                "status": event.status,
            }
            for event in events
        ]
    }
