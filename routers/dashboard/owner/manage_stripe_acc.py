
# from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from financials.stripe.crud.store_account_id import get_owner_stripe_account
from security.access_control.auth.dependencies.session_control import validate_user_account
from security.access_control.crud_db.get_primary_owner_email import get_primary_owner_email_by_id
from financials.stripe.landloards_acc_mng import setup_landlord_account, create_express_dashboard, delete_stripe_account, create_express_session


stripe_router = APIRouter(
    prefix="/stripe",
    tags=["stripe"],
    responses={404: {"description": "Not found"}}
)



@stripe_router.post('/create-account')
async def create_account(backgroundtasks:BackgroundTasks, uid:str=Depends(validate_user_account)):
    '''
    Landlords create their accounts using this endpoint.

    :params:backgroundTasks
    :params:session

    :return:dict account.id, account_link.url
    '''

    # Get landlords email address.
    email:str = await get_primary_owner_email_by_id(uid)
    
    # create account link
    onboarding_link = await setup_landlord_account(uid, email, backgroundtasks)
    return onboarding_link


@stripe_router.post('/view-account')
async def view_account(uid:str=Depends(validate_user_account)):
    '''
    Landlords create their accounts using this endpoint.
    :params:uid

    :return:dict account.id, account_link.url
    '''

    # create account link
    onboarding_link = await create_express_dashboard(uid)
    return onboarding_link


@stripe_router.post('/account-session')
async def account_session(uid:str=Depends(validate_user_account)):
    '''
    Landlords create their accounts using this endpoint.
    :params:uid

    :return:dict account.id, account_link.url
    '''

    # create account link
    onboarding_link = await create_express_session(uid)
    return onboarding_link


@stripe_router.delete('/delete-account')
async def delete_account(uid:str=Depends(validate_user_account)):
    '''
    Landlords deletes their accounts using this endpoint.

    :params:backgroundTasks
    :params:session

    :return:dict 
    '''
    message = await delete_stripe_account(uid)
    return message

@stripe_router.post('/validate-account')
async def delete_account(uid:str=Depends(validate_user_account)):
    '''
    Validates the user's stripe account.
    '''
    result = await get_owner_stripe_account(uid)
    is_account = bool(result)
    output = 633 if is_account else 564
    return dict(account_status=output)