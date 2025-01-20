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
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Owner(Base):
    '''User table model'''
    __tablename__= "owners"
    id=Column(Integer, primary_key=True)
    firstname=Column(String)
    lastname=Column(String)
    email=Column(String)
    phone=Column(String)
    country=Column(String)
    province=Column(String)
    city=Column(String)
    address=Column(String)
    unit=Column(Integer)
    password=Column(String)
    verification=Column(String)


class Tenants(Base):
    '''User table model'''
    __tablename__= "tenants"
    id=Column(Integer, primary_key=True)
    firstname=Column(String)
    lastname=Column(String)
    dob=Column(Date)
    email=Column(String)
    phone=Column(String)
    password=Column(String)
    property_id=Column(String)
    occupation=Column(String)
    company=Column(String)
    salary=Column(Integer)
    verification=Column(String)