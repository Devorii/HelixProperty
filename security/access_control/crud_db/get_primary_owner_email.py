
from fastapi import HTTPException
from sqlalchemy import select
from database_ops.db_connection import get_db
from property_management.models.properties_table import Properties
from models.users import Owner



async def get_primary_owner_email(assets):
    '''
    Get primary owner's email

    :params dict:assets
    '''
    try: 
        with get_db() as db:
      
            query=select(Properties.primary_owner).where(Properties.property_code==assets)
            primary_owner_id=db.execute(query).fetchone()
       
  
            get_primary_owner_email_address=select(Owner.email).where(Owner.id==primary_owner_id[0])
            prime_owner_email=db.execute(get_primary_owner_email_address).fetchone()

     
            return prime_owner_email[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    


async def get_primary_owner_email_by_id(user_id:int) -> str:
    '''
    Get primary owner's email

    :params dict:assets
    :return:str email
    '''
    try: 
        with get_db() as db:
            get_primary_owner_email_address=select(Owner.email).where(Owner.id==user_id)
            prime_owner_email=db.execute(get_primary_owner_email_address).fetchone()

            return prime_owner_email[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")