from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import EnPackageCategories, EnPackageSubcategories
from core.security import ( validate_common_request, verify_access_token )
from schemas.common import CommonRequest

from core.security import get_current_user

router = APIRouter(
    prefix="/packages",
    tags=["packageInfo"]
)

optional_bearer = HTTPBearer(auto_error=False)

@router.post("/categories")
def get_category_list(
    request: CommonRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
    db: Session = Depends(get_db)
):
    # Validate JWT only when token is provided
    current_user = None

    if credentials is not None:
        token = credentials.credentials
        current_user = verify_access_token(token)

        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

    # Validate common request
    validate_common_request(request, "login")

    # Fetch categories
    query = db.query(EnPackageCategories)

    # Without token: active packages only
    if current_user is None:
        query = query.filter(
            EnPackageCategories.status == 1
        )

    categories = query.order_by(
        EnPackageCategories.id.asc()
    ).all()

    return {
        "status": True,
        "message": "Categories fetched successfully",
        "data": [
            {
                "id": cat.id,
                "package_name": cat.package_name,
                "status": cat.status,
                "datecreated": cat.datecreated,
            }
            for cat in categories
        ]
    }

@router.post("/subCategories")
def get_subCategory_list(
    request: CommonRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
    db: Session = Depends(get_db)
):
    # 1. Validate JWT only when token is provided
    current_user = None

    if credentials is not None:
        token = credentials.credentials
        current_user = verify_access_token(token)

        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

    # 2. Validate common request
    validate_common_request(request, "login")

    # 3. Get category ID if provided
    params = request.params or {}
    category_id = params.get("main_catid")

    # 4. Join categories and subcategories tables
    query = (
        db.query(
            EnPackageCategories.id.label("category_id"),
            EnPackageCategories.package_name,
            EnPackageSubcategories.cid,
            EnPackageSubcategories.main_catid,
            EnPackageSubcategories.subcatname,
            EnPackageSubcategories.created_at,
            EnPackageSubcategories.updated_at,
            EnPackageSubcategories.status
        )
        .join(
            EnPackageCategories,
            EnPackageCategories.id == EnPackageSubcategories.main_catid
        )
    )

    # 5. Without token: return active categories and subcategories only
    if current_user is None:
        query = query.filter(
            EnPackageCategories.status == 1,
            EnPackageSubcategories.status == "1"
        )

    # 6. If category ID is provided, filter by that category
    if category_id is not None:
        try:
            category_id = int(category_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Invalid category ID"
            )

        query = query.filter(
            EnPackageCategories.id == category_id
        )

    # 7. Fetch all matching records
    subCategories = query.order_by(
        EnPackageSubcategories.cid.asc()
    ).all()

    # 8. Return response
    return {
        "status": True,
        "message": "SubCategories fetched successfully",
        "data": [
            {
                "category_id": subCat.category_id,
                "package_name": subCat.package_name,
                "cid": subCat.cid,
                "main_catid": subCat.main_catid,
                "subcatname": subCat.subcatname,
                "created_at": subCat.created_at,
                "updated_at": subCat.updated_at,
                "status": subCat.status,
            }
            for subCat in subCategories
        ]
    }

@router.post("/frontend/subCategories")
def get_frontend_subcategories(
    request: CommonRequest,
    db: Session = Depends(get_db)
):
    # Validate common request
    validate_common_request(request, "login")

    # Get selected category ID
    category_id = request.params.get("main_catid")

    if not category_id:
        return {
            "status": False,
            "message": "Category ID is required",
            "data": []
        }

    # Validate category ID
    try:
        category_id = int(category_id)
    except (ValueError, TypeError):
        return {
            "status": False,
            "message": "Invalid Category ID",
            "data": []
        }

    # SQLAlchemy ORM JOIN
    subcategories = (
        db.query(
            EnPackageCategories.id.label("category_id"),
            EnPackageCategories.package_name,
            EnPackageSubcategories.cid,
            EnPackageSubcategories.main_catid,
            EnPackageSubcategories.subcatname,
            EnPackageSubcategories.created_at,
            EnPackageSubcategories.updated_at,
            EnPackageSubcategories.status
        )
        .join(
            EnPackageSubcategories,
            EnPackageCategories.id == EnPackageSubcategories.main_catid
        )
        .filter(
            EnPackageCategories.id == category_id,
            EnPackageCategories.status == 1,
            EnPackageSubcategories.status == "1"
        )
        .order_by( EnPackageSubcategories.cid.asc() )
        .all()
    )

    # Convert SQLAlchemy result into JSON response
    data = [
        {
            "category_id": row.category_id,
            "package_name": row.package_name,
            "cid": row.cid,
            "main_catid": row.main_catid,
            "subcatname": row.subcatname,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "status": row.status
        }
        for row in subcategories
    ]

    return {
        "status": True,
        "message": "Subcategories fetched successfully",
        "data": data
    }
