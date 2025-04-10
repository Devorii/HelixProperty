"""
Module Name: triage_comment.py
Description: Comment model for database.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2025-04-08
Last Modified: 2025-04-08


Dependencies:
    - sqlalchemy >= 2.0.27
    - cachetools >= 5.5.x
"""

from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Comments(Base):
    '''Comments table model'''
    __tablename__= "comments_list"
    id_comments=Column(Integer, primary_key=True, autoincrement=True)
    fullname=Column(String)
    initials=Column(String)
    property_id=Column(String)
    ticket_id=Column(String)
    created_date=Column(Date)
    role=Column(String)
    notes=Column(Text)
