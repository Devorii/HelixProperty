
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
from database_ops.db_connection import Base


class Properties(Base):
    '''Owner property table model'''
    __tablename__= "properties"
    idproperties=Column(Integer, primary_key=True)
    property_code=Column(String(255))
    country=Column(String(255))
    province=Column(String(255))
    city=Column(String(255))
    address=Column(String(255))
    unit=Column(Integer)
    primary_owner=Column(String(255))
    other_owners=Column(String(255))
    stripe_account=Column(String(255))