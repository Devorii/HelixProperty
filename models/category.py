from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Categories(Base):
    '''User table model'''
    __tablename__= "categories"
    idcategories=Column(Integer, primary_key=True)
    name=Column(String)
    unique_id=Column(String)
