from datetime import datetime, timedelta, timezone
import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError


load_dotenv()


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "happy123"
)

ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)

AUTH_KEY = os.getenv("AUTH_KEY")


security = HTTPBearer()


# --------------------------------
# Create JWT
# --------------------------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "jti": str(uuid4())
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# --------------------------------
# Verify JWT
# --------------------------------

def verify_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# --------------------------------
# Common API Validation
# --------------------------------

def validate_common_request(
    request,
    expected_type: str
):

    data = request.model_dump()

    request_type = data.get("type")
    request_key = data.get("Authkey")

    if request_type != expected_type:

        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )

    if request_key != AUTH_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid request"
        )

    return True


# --------------------------------
# JWT Authentication
# --------------------------------

def get_current_user( credentials: HTTPAuthorizationCredentials = Depends(security) ):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload
