
"""
Module Name: add_ticket_imgs.py
Description: Adds images pushed with a ticket to the database.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-02-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.ticket_img_models import TicketsImgUrl



async def add_ticket_imgs(img_metadata:dict):
    '''
    Add images to the database.
    '''
    try: 
        with get_db() as db:
            db.add(TicketsImgUrl(**img_metadata))
            db.commit()
            print('Ticket images have been submitted.')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    pass
