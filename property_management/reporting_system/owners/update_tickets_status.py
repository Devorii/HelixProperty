
"""
Module Name: update_ticket_status.py
Description: update reports - Triage tickets.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-01-20


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.triage_tickets import Triage_tickets
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from models.users import Owner, Tenants
from property_management.models.properties_table import Properties


async def update_ticket_status(ticket_info):
    '''
    updates a ticket to our system.
    '''
    try: 
        with get_db() as db:
            query=update(Triage_tickets).where(Triage_tickets.ticket_num==ticket_info['ticket_num']).values(status=ticket_info['status'])
            db.execute(query)
            db.commit()


            # Get other admin email
            get_admins_email=select(Properties.other_owners, Properties.primary_owner).where(Properties.property_code==ticket_info['property_id'])
            other_mail=db.execute(get_admins_email).fetchall()
            admin_ids_ls=[id for ids in other_mail[0] for id in ids.split(',')]
            admin_emails=db.query(Owner.email).filter(Owner.id.in_(admin_ids_ls)).all()
            list_of_emails=[emails[0] for emails in admin_emails]
         
            
            tenant_email=select(Tenants.email).where(Tenants.property_id==ticket_info['property_id'])
            tenants_email=db.execute(tenant_email).fetchall()
            tenants_emails=[emails for emails in tenants_email[0]]

            ls=list_of_emails + tenants_emails
        return ls
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
