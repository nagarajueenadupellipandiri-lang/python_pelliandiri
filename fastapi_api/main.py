from fastapi import FastAPI
from sqlalchemy import text
from database import engine
from models import User,EnLogin
from routes.auth import router as auth_router
from routes.theme import router as theme_router
from routes.employees import router as employees_router
from routes.parichayavedicaEvents import router as parichayavedicaEvents_router
from routes.registrations import router as registrations_router
from routes.location import router as location_router
from routes.socioReligious import router as socioReligious_router
from routes.basicInfo import router as basicInfo_router
from routes.educationDetails import router as educationDetails_router
from routes.employmentDetails import router as employmentDetails_router

app = FastAPI( title="Pellipandiri API", version="1.0.0" )

app.include_router(theme_router)
app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(parichayavedicaEvents_router)
app.include_router(registrations_router)
app.include_router(basicInfo_router)
app.include_router(location_router)
app.include_router(socioReligious_router)
app.include_router(educationDetails_router)
app.include_router(employmentDetails_router)

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

        return {
            "status": True,
            "message": "MySQL connected successfully",
            "result": value
        }

    except Exception as e:
        return {
            "status": False,
            "message": "MySQL connection failed",
            "error": str(e)
        }


