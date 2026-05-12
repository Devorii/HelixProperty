"""
Module Name: users.py
Description: Defines our user models.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
    - cachetools >= 5.5.x
"""

from sqlalchemy import Column, String, Integer, Date
from database_ops.db_connection import Base


class Owner(Base):
    '''User table model'''
    __tablename__= "owners"
    id=Column(Integer, primary_key=True)
    firstname=Column(String(255))
    lastname=Column(String(255))
    email=Column(String(255))
    phone=Column(String(255))
    country=Column(String(255))
    province=Column(String(255))
    city=Column(String(255))
    address=Column(String(255))
    unit=Column(Integer)
    password=Column(String(255))
    verification=Column(String(255))
    stripe_account_id=Column(String(255))


class Tenants(Base):
    '''User table model'''
    __tablename__= "tenants"
    id=Column(Integer, primary_key=True)
    firstname=Column(String(255))
    lastname=Column(String(255))
    dob=Column(Date)
    email=Column(String(255))
    phone=Column(String(255))
    password=Column(String(255))
    property_id=Column(String(255))
    occupation=Column(String(255))
    company=Column(String(255))
    salary=Column(Integer)
    verification=Column(String(255))