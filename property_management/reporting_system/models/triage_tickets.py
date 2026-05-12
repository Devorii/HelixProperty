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
from database_ops.db_connection import Base


class Triage_tickets(Base):
    '''Issue table model'''
    __tablename__= "triage_tickets"
    id=Column(Integer, primary_key=True)
    category=Column(String(255))
    title=Column(String(255))
    description=Column(Text)
    created_date=Column(Date)
    author_id=Column(Integer)
    author=Column(String(255))
    status=Column(String(255))
    property_id=Column(String(255))
    ticket_num=Column(String(255))