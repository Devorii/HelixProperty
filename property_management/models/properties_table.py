
"""
Module Name: properties.py
Description: Declares owners property interface for sqlachemy.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Properties(Base):
    '''Owner property table model'''
    __tablename__= "properties"
    idproperties=Column(Integer, primary_key=True)
    property_code=Column(String)
    country=Column(String)
    province=Column(String)
    city=Column(String)
    address=Column(String)
    unit=Column(Integer)
    primary_owner=Column(String)
    other_owners=Column(String)
    stripe_account=Column(String)