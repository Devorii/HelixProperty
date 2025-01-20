"""
Module Name: add_property.py
Description: Inject property data into database on account creation.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
    - cachetools >= 5.5.x
"""

from fastapi import HTTPException
from database_ops.db_connection import get_db
from models.users import Owner, Tenants
from property_management.models.properties_table import Properties
from sqlalchemy import select
import uuid

user_account = {'OW1':Owner, 'TE1': Tenants}

async def add_property(property:dict):
    ''' Creates new proprty'''
    # Generate random property code
    random_propery_loc_number= str(uuid.uuid4())[0:13].replace("-","")
    try:
        with get_db() as db:
            query = select(Owner.id).where(Owner.email==property["email"])
            property.pop('occupation', None) 
            property.pop('account', None)
            property.pop('email', None)
            result=db.execute(query).fetchone()

            if property['primary_owner'] != "false":
                property['primary_owner']=result[0]
                
            else:  
                property['primary_owner']=0
                property['other_owners']=result[0]
                
            property['property_code']=random_propery_loc_number
            db.add(Properties(**property))
            db.commit()
        return random_propery_loc_number
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")