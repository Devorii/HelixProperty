from pydantic import BaseModel


class Create_user_request(BaseModel):
    firstname:str
    lastname: str
    email: str
    phone: str
    password: str
    country: str
    province: str
    city: str
    address: str
    account:str
    unit: int

class Login(BaseModel):
    email:str
    password:str
    account:str
