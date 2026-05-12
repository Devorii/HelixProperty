
"""
Module Name: model.py
Description: Declares rent interface for sqlachemy.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""

from sqlalchemy import Column, String, Integer, DATETIME
from database_ops.db_connection import Base


class Rent(Base):
    '''Owner property table model'''
    __tablename__= "tentant_rent"
    rent_id=Column(Integer, primary_key=True)
    prop_id=Column(String(255))
    tenant_id=Column(Integer)
    rental_price=Column(String(255))
    creation_date=Column(DATETIME)
    last_update=Column(DATETIME)