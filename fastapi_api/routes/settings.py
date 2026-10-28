from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (EnBanners) 
from core.security import ( validate_common_request, get_current_user, )
from schemas.common import CommonRequest

router = APIRouter( prefix="/SiteSettings", tags=["logoAndBanners"] )

@router.post("/banners")
def get_banners_list(
    request: CommonRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_common_request(request, "login")
    banners = (
        db.query(EnBanners)
        .all()
    )

    return {
        "status": True,
        "message": "Banners fetched successfully",
        "data": [
            {
                "id": bl.id,
                "banner_type": bl.banner_type,
                "title": bl.title,
                "description": bl.description,
                "image": bl.image,
                "alttext": bl.alttext,
                "caption": bl.caption,
                "status": bl.status,
                "created_at": bl.created_at,
                "updated_at": bl.updated_at,
                "alttstatusext": bl.status,
                "deleted": bl.deleted,
            }
            for bl in banners
        ]
    }