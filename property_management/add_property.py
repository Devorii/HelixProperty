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
from sqlalchemy import select, update
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
            property['other_owners'] = ''
    
            result=db.execute(query).fetchone()

            property['primary_owner']=result[0]
            property['property_code']=random_propery_loc_number
            db.add(Properties(**property))
            db.commit()
        return random_propery_loc_number
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    

async def add_user_to_property(property:dict):

    try:
        with get_db() as db:
            query = select(Owner.id).where(Owner.email==property["email"])
            property.pop('occupation', None) 
            property.pop('account', None)
            property.pop('email', None)
            admin_id=db.execute(query).first()
            if not admin_id:
                raise ValueError("Admin not found for the provided email")
            admin_id = admin_id[0]


            get_property_other_admin=select(Properties.other_owners).where(Properties.property_code==property['property_code'])
            non_primary_owner=db.execute(get_property_other_admin).first()
            non_primary_owner = non_primary_owner[0] if non_primary_owner else None

            # Build the new list of admin_ids
            if not non_primary_owner:
                admin_ids = str(admin_id)
            else:
                owners_list = non_primary_owner.split(',')
                if str(admin_id) not in owners_list:
                    owners_list.append(str(admin_id))
                admin_ids = ','.join(owners_list)

                
            
            updateProperties=update(Properties).where(Properties.property_code==property['property_code']).values(other_owners=admin_ids)
            db.execute(updateProperties)
            db.commit()

        return property['property_code']
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")