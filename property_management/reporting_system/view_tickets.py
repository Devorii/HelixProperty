
"""
Module Name: view_ticket.py
Description: view reports of associated to a property - Triage tickets.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-01-16


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.triage_tickets import Triage_tickets
from property_management.reporting_system.models.ticket_view_model import TicketModel
from sqlalchemy import select


async def view_tickets(property_ref:dict) -> list:
    '''
   view a tickets in our system.
   :params dict:property_ref

   :return list:output
    '''
    try: 
        with get_db() as db:
            output=[]
            # Get owners email
            query=select(Triage_tickets).where(Triage_tickets.property_id==property_ref['property_id'])
            tickets=db.execute(query).fetchall()
            list_of_cols=["ticket", "id", "category", "title", "decription", "created_date", "author_id", "author", "status", "property_id", "ticket_num"]
            ticket=dict()
            for items in tickets: 
                for name, value in zip(list_of_cols, items):
                    ticket[name]=value
                output.append(ticket['ticket']) 
        return output
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    



