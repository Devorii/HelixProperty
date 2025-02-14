from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class TicketsImgUrl(Base):
    '''Img url table model'''
    __tablename__= "tickets_images_url"
    id=Column(Integer, primary_key=True)
    property_id=Column(String)
    ticket_number=Column(String)
    images_url=Column(String)
    created_on=Column(Date)

