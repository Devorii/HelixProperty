
"""
Module Name: store_account_id.py
Description: Handles stipe db operations.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-01-20


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from database_ops.db_connection import get_db
from sqlalchemy import select, update
from models.users import Owner, Tenants
from property_management.rent.model.model import Rent
from property_management.models.properties_table import Properties


async def update_owner_stripe_account(uid:int, stripe_acc_id:str):
    '''
    updates owners stripe account
    '''
    try: 
        with get_db() as db:
            query=update(Owner).where(Owner.id==uid).values(stripe_account_id=stripe_acc_id)
            db.execute(query)
            db.commit()

        print('Stripe account updated.')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    

async def get_owner_stripe_account(uid:str):
    '''
    gets owners stripe account
    '''
    try: 
        with get_db() as db:
            query=select(Owner.stripe_account_id).where(Owner.id==uid)
            account=db.execute(query).fetchone()
        
        return account[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
        


async def get_owner_stripe_account_with_prop_id(prop_id:str):
    '''
    gets property stripe account
    '''
    try: 
        with get_db() as db:
            query=select(Properties.primary_owner).where(Properties.property_code == prop_id)
            result=db.execute(query).fetchone()
            owner_account_id = result[0]

            stripe_query = select(Owner.stripe_account_id, Owner.email).where(Owner.id==owner_account_id)
            stripe_result = db.execute(stripe_query).fetchone()

        return dict(account=stripe_result[0], email=stripe_result[1])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    

async def get_single_tenant_rent_info(uid):
    '''
    '''
    try: 
        with get_db() as db:
            query=select(Tenants).where(Tenants.id==uid)
            result=db.execute(query).fetchone()
            single_tenant_metadata = result[0]

            prop_query=select(Properties.address).where(Properties.property_code==single_tenant_metadata.property_id)
            prop_result = db.execute(prop_query).fetchone()
            prop_address=prop_result[0]


            return dict(fname=single_tenant_metadata.firstname, lname=single_tenant_metadata.lastname, address=prop_address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")