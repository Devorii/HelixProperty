from sqlalchemy import Column, String, Integer, Date, Text
from database_ops.db_connection import Base


class Vendors(Base):
    '''Vendors table model'''
    __tablename__= "vendors"
    idvendors=Column(Integer, primary_key=True)
    name=Column(String(255))
    category=Column(String(255))
    street_address=Column(String(255))
    city=Column(String(255))
    province=Column(String(255))
    country=Column(String(255))
    postal_zip=Column(String(255))
    phone=Column(String(255))
    email=Column(String(255))
    unique_id=Column(String(255))
    long=Column(String(255))
    lat=Column(String(255))

class FavoriteVendors(Base):
    '''Favorite vendors table model'''
    __tablename__= "favorite_vendors"
    id=Column(Integer, primary_key=True)
    user_id=Column(String(255))
    vendor_id=Column(String(255))

