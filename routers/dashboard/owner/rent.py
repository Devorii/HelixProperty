
# from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.rent.rental_management import update_tenants_rent


rent_router = APIRouter(
    prefix="/rent",
    tags=["stripe"],
    responses={404: {"description": "Not found"}}
)


@rent_router.post('/update')
async def update_rent(rental_info:dict, backgroundtasks:BackgroundTasks, uid:str=Depends(validate_user_account)):
    '''
    Checks and updates tenant's rental information.

    :params:backgroundTasks
    :params:uid

    :return:dict account.id, account_link.url
    '''    
    message=await update_tenants_rent(rental_info)    
    return dict(message=message)

