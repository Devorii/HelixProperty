from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Vendors(Base):
    '''Vendors table model'''
    __tablename__= "vendors"
    idvendors=Column(Integer, primary_key=True)
    name=Column(String)
    category=Column(String)
    street_address=Column(String)
    city=Column(String)
    province=Column(String)
    country=Column(String)
    postal_zip=Column(String)
    phone=Column(String)
    email=Column(String)
    unique_id=Column(String)


