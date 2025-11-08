"""
Module Name: rental_management.py
Description: updates tenant's rent information.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2025-05-01
Last Modified: 2025-05-24


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from datetime import datetime
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.rent.model.model import Rent
from sqlalchemy import select, update


async def get_tenants_rent_info(prop_id, tenant_id):
    try: 
        with get_db() as db:
            query=select(Rent.rental_price).where(Rent.prop_id == prop_id, Rent.tenant_id == tenant_id)
            result = db.execute(query).fetchone()

            if result:
                return str(result[0])
            return '0'
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was a problem fetching users - {e}")   





    
           

async def update_tenants_rent(rent_info):
    """
    Inserts or updates a tenant's rental information in the database.

    This function checks if a rental record already exists for the given tenant.
    - If a record exists, it updates the `rental_price` with the new amount.
    - If no record exists, it creates a new `Rent` entry with the provided 
      property ID, tenant ID, rental price, and current timestamp.

    Args:
        rent_info (dict): A dictionary containing tenant and rental details with keys:
            - 'prop_id' (int): The property ID associated with the tenant.
            - 'tenant_id' (int): The unique identifier of the tenant.
            - 'amount' (float): The rental price to set for the tenant.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If there is any problem fetching or updating tenant data.
    """
    try: 
        with get_db() as db:
            tenant=select(Rent).where(Rent.tenant_id==rent_info.get('tenant_id'))
            result=db.execute(tenant).fetchone()
            is_tenant_price_set = bool(result)

            if not is_tenant_price_set:
                create_rent_data = Rent(
                    prop_id=rent_info.get('prop_id'),
                    tenant_id=rent_info.get('tenant_id'),
                    rental_price=rent_info.get('amount'),
                    creation_date=rent_info.get('created_on')
                )
                db.add(create_rent_data)
            else:
                update_rent_data=update(Rent).where(Rent.tenant_id==rent_info.get('tenant_id')).values(rental_price = rent_info.get('amount'), last_update = rent_info.get('created_on'))
                db.execute(update_rent_data)
            db.commit()
        return dict(message='Tenant rent has been updated.')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was a problem fetching users - {e}")
    
