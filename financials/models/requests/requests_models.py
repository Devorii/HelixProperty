from pydantic import BaseModel



class ItemsModel(BaseModel):
    item:str
    description:str
    quantity:int
    price: str
    amount: str
    report_id:str