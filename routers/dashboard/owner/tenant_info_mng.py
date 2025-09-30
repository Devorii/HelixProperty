
import base64
from datetime import datetime
from fastapi import APIRouter, Depends
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.contacts.contacts import get_tenants_information, delete_tenants_information

contact_info_router = APIRouter(
    prefix="/tenant",
    tags=["tenant"],
    responses={404: {"description": "Not found"}}
)



@contact_info_router.post('/view-info')
async def create_comment(payload:dict, session:str=Depends(validate_user_account)):
    '''sdxzsseszsszgff123
    create comments

    :params dict:payload {property_id}
    :params str:session

    :return str
    '''
    date=datetime.now()
    data=dict(property_id=payload['property_id'])

    property_contacts=await get_tenants_information(data)

    return property_contacts


@contact_info_router.post('/remove')
async def create_comment(payload:dict, session:str=Depends(validate_user_account)):
    '''
    create comments

    :params dict:payload {uid}
    :params str:session

    :return str
    '''
    uid=int(base64.b64decode(payload['uid']))
    return await delete_tenants_information(uid)