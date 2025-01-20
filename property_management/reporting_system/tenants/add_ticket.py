
"""
Module Name: add_ticket.py
Description: Adds reports of an issue to property issue table - Triage tickets.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-01-15


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.triage_tickets import Triage_tickets
from sqlalchemy import select
from models.users import Owner
from property_management.models.properties_table import Properties
from property_management.reporting_system.email_notifications.new_ticket_notification import Create_email_notification


async def add_ticket(ticket_info):
    '''
    Adds a ticket to our system.
    '''
    try: 
        with get_db() as db:
            db.add(Triage_tickets(**ticket_info))
            db.commit()

            # Get owners email
            query=select(Properties.primary_owner).where(Properties.property_code==ticket_info['property_id'])
            owner_id=db.execute(query).fetchone()
            
            owner_query=select(Owner.email).where(Owner.id==owner_id[0])
            raw_email=db.execute(owner_query).fetchone()

        return raw_email[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    pass



