
from fastapi import HTTPException
from sqlalchemy import select, or_
from database_ops.db_connection import get_db
from property_management.models.properties_table import Properties
from models.users import Tenants




async def get_property_metadata(assets:dict):
    '''
    Get's property id associated to with uid

    :params dict:assets
    '''
    properties_metadata=[]
    try: 
        with get_db() as db:
            query=select(Properties).where(or_(Properties.primary_owner==assets['uid'], Properties.other_owners.ilike(f'%{assets["uid"]}%')))
            property=db.execute(query).fetchall()

            for metadata in property:
                np=metadata[0]
                # print(metadata[0].property_code)
                properties_metadata.append([f"{np.address} {np.city} - Unit {np.unit}", np.property_code])
            
            return properties_metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    