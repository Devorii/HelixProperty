from pydantic import BaseModel


class TicketModel(BaseModel):
    id:int
    category:str
    title:str
    description:str
    created_date:str
    author_id:int
    author:str
    status:str
    property_id:str
    ticket_num: int
