"""
Module Name: triage_tickets.py
Description: Defines our issue models.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-13


Dependencies:
    - sqlalchemy >= 2.0.27
    - cachetools >= 5.5.x
"""

from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Triage_tickets(Base):
    '''Issue table model'''
    __tablename__= "triage_tickets"
    id=Column(Integer, primary_key=True)
    category=Column(String)
    title=Column(String)
    description=Column(Text)
    created_date=Column(Date)
    author_id=Column(Integer)
    author=Column(String)
    status=Column(String)
    property_id=Column(String)
    ticket_num=Column(String)