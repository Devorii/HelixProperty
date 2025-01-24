from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Annotated
from models.request import Login
from models.repsonse import Create_account_response
from dependencies.ca_formatting_validation import payload_validation
from security.access_control.auth.login import user_login_method
from security.access_control.crud_db.user_access import add_user, get_uid
from security.access_control.crud_db.account_access import verify_accounts
from property_management.add_property import add_property
from security.encryption.handler import Encryption_handler, Generate_random_hash
from notification_protocols.email import Create_email_notification
from security.access_control.crud_db.get_property_id import get_property_id
from security.access_control.auth.dependencies.session_control import validate_user_account
import redis

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)

@router.post('/validate-home')
async def validate_home(validate_token:str=Depends(validate_user_account)):
    return 'Access Granted'


@router.post("/create-account")
async def create_account(user_data: Annotated[dict, Depends(payload_validation)], background_task:BackgroundTasks):
    ''' CREATES USERS ACCOUNTS'''
    try: 
        account = str(user_data['account'])
        property_obj=dict( 
        email=user_data['email'],
        country=user_data['propCountry'],
        province=user_data['propProvince'],
        city=user_data['propCity'],
        address=user_data['propAddress'],
        unit=user_data['unit'],
        primary_owner=user_data['po'],
        other_owners="")


        user_data.pop('propCountry', None)
        user_data.pop('propProvince', None)
        user_data.pop('propCity', None)
        user_data.pop('propAddress', None)
        user_data.pop('unit', None)
        user_data.pop('po', None)


        random_hash = Generate_random_hash()    
        hashed = random_hash.generate()
        crop_hash=hashed[:10]
        user_data['verification']=crop_hash

        
        
        if account != "TE1":
            user_data.pop('salary', None) 
            user_data.pop('occupation', None) 
            user_data.pop('dob', None) 
            user_data.pop('company', None) 
            user_data.pop('code', None)     

            await add_user(user_data)
            prop_id=await add_property(property_obj)

        else:
            prop_id=user_data['code']
            user_data['salary']=user_data['salary'].replace(',','').replace('$','')
            user_data.pop('country', None) 
            user_data.pop('propAddress', None) 
            user_data.pop('city', None) 
            user_data.pop('province', None) 
            user_data.pop('address', None) 
            user_data.pop('propCity', None) 
            user_data.pop('propProvince', None) 
            user_data.pop('unit', None) 
            user_data.pop('po', None)   
            user_data['property_id']=user_data['code']
            user_data.pop('code', None)
            await add_user(user_data)

        token = await get_uid(user_data['email'], account)
        email_artifacts = dict(email=user_data['email'], name=user_data['firstname'], hash_code=crop_hash, account=account, token=token, propId=prop_id)
        # # # Send email as background task.

        create_notificaiton = Create_email_notification(email_artifacts)
        background_task.add_task(create_notificaiton.send_mail)
        return Create_account_response(status_code=200, token=str(token), detail=f"Successful! Account created.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Bad request - {e}')



@router.post("/login")
async def login(payload:Annotated[Login, Depends(user_login_method)]):
    property_assets=dict(uid=payload['uid'], account=payload['account'])
    property_id=await get_property_id(property_assets)
    payload['property_id']=property_id
    _,_=payload.pop('uid'),payload.pop('account')
    return payload


@router.get("/verify-accout/{code}/{account}/{token}")
async def verify_account(code:str, account:str, token:str):
    instantiate_decryption=Encryption_handler(token, "password")
    uid = instantiate_decryption.decrypt()
    resp = await verify_accounts(dict(account=account, uid=uid, hash=code))
    return resp