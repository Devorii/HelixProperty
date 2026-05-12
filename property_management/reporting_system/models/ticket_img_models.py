from sqlalchemy import Column, String, Integer, Date
from database_ops.db_connection import Base


class TicketsImgUrl(Base):
    '''Img url table model'''
    __tablename__= "tickets_images_url"
    id=Column(Integer, primary_key=True)
    property_id=Column(String(255))
    ticket_number=Column(String(255))
    images_url=Column(String(255))
    created_on=Column(Date)

