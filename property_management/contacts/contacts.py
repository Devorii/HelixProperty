











"""
Module Name: contacts.py
Description: Tenant contact file.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2025-05-01
Last Modified: 2025-05-24


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from datetime import datetime, date
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.triage_tickets import Triage_tickets
from sqlalchemy import select, delete
from models.users import Tenants
from property_management.rent.rental_management import get_tenants_rent_info
from models.users import Tenants


async def get_tenants_information(property_info):
    '''
    Collects tenants information. 
    '''
    try: 
        with get_db() as db:
            output=[]
            tenant=select(Tenants).where(Tenants.property_id==property_info['property_id'])
            tenants=db.execute(tenant).fetchall()

            for tenants_info in tenants:
                rental_price = await get_tenants_rent_info(property_info.get('property_id'), tenants_info[0].id)
                tenant_data=tenants_info[0]
                fname,lname=tenant_data.firstname, tenant_data.lastname
                initials=fname[0]+lname[0]
                today=date.today()
                tnt_dob=datetime.fromisoformat(str(tenant_data.dob))
                tnt_age=today.year - tnt_dob.year - ((today.month, today.day) < (tnt_dob.month, tnt_dob.day))
                groom_data=dict(
                    uid=tenant_data.id,
                    rental_price=rental_price,
                    intials=initials, 
                    fullname=f"{fname} {lname}", 
                    email=tenant_data.email,
                    dob=tnt_dob.date(), 
                    age=tnt_age,
                    phone=tenant_data.phone, 
                    occupation=tenant_data.occupation, 
                    company=tenant_data.company)

                output.append(groom_data)
        return output
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was a problem fetching users - {e}")
    


async def delete_tenants_information(uid):
    '''
    Collects tenants information. 
    '''
    try: 
        with get_db() as db:
            tenant=delete(Tenants).where(Tenants.id==uid)
            db.execute(tenant)
            db.commit()

        return "User has been removed."
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was a problem deleting user - {e}")