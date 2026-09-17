from typing import Any
from pydantic import BaseModel, Field

class CommonRequest(BaseModel):

    type: str = Field( default="login", )
    Authkey: str = Field( default="pppudanee", )
    params: dict[str, Any] = Field( default_factory=dict, examples=[{}] )