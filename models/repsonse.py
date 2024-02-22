from pydantic import BaseModel


class Create_account_response(BaseModel):
    token: str
    status_code: int
    detail: str