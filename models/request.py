from pydantic import BaseModel
from typing import List


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

class expense_payload(BaseModel):
    billNumber:str
    calculations:dict
    category:str
    currency:str
    dueDate:str
    items:List
    posoNumber:str
    timestamp:str
    vendor:str
    propID:str
