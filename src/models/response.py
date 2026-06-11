from typing import Literal
from pydantic import BaseModel


class RulateResponse(BaseModel):
    msg: str
    status: Literal["success", "fail"]
    response: dict | list | None
