from pydantic import BaseModel

class LoginParams(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    type: str
    Authkey: str
    params: LoginParams

class LogoutParams(BaseModel):
    pass

class LogoutRequest(BaseModel):
    type: str
    Authkey: str
    params: LogoutParams
