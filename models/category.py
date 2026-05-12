from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from database_ops.db_connection import Base



class Categories(Base):
    '''User table model'''
    __tablename__= "categories"
    idcategories=Column(Integer, primary_key=True)
    name=Column(String(255))
    unique_id=Column(String(255))
