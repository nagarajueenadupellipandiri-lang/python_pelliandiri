from fastapi import FastAPI
from sqlalchemy import text
from database import engine
from models import User,EnLogin
from routes.auth import router as auth_router
from routes.theme import router as theme_router
from routes.employees import router as employees_router
from routes.parichayavedicaEvents import router as parichayavedicaEvents_router
from routes.registrations import router as registrations_router
from routes.casteMaster import router as casteMaster_router
from routes.religionMaster import router as religionMaster_router
from routes.heightMaster import router as heightMaster_router

app = FastAPI( title="Pellipandiri API", version="1.0.0" )

app.include_router(theme_router)
app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(parichayavedicaEvents_router)
app.include_router(registrations_router)
app.include_router(casteMaster_router)
app.include_router(religionMaster_router)
app.include_router(heightMaster_router)

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


