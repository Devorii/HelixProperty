
from fastapi import HTTPException
from sqlalchemy import select
from database_ops.db_connection import get_db
from property_management.models.properties_table import Properties
from models.users import Tenants



async def get_property_id(assets:dict):
    '''
    Get's property id associated to with uid

    :params dict:assets
    '''
    try: 
        with get_db() as db:
            if assets['account'] != "TE1":
                query=select(Properties.property_code).where(Properties.primary_owner==assets['uid'])
            else:
                query=select(Tenants.property_id).where(Tenants.id==assets['uid'])
            
            property_code=db.execute(query).fetchone()
            return property_code[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    


