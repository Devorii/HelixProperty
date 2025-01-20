

from pydantic import BaseModel


class CreateTicket(BaseModel):
    category:str
    title:str
    description:str
    author_id:int
    author:str
    property_id:str