from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Annotated
from models.request import Create_user_request, Login
from models.repsonse import Create_account_response
from dependencies.ca_formatting_validation import payload_validation
from dependencies.authorization import validate_user_account, user_login_method
from database_ops.crud.admin import add_user, get_uid, verify_accounts
from encryption.handler import Encryption_handler, Generate_random_hash
from notification_protocols.email import Create_email_notification

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)

@router.post("/create-account")
async def create_account(user_data: Annotated[dict, Depends(payload_validation)], background_task:BackgroundTasks) -> Create_account_response:
    ''' CREATES USERS ACCOUNTS'''
    try: 
        account = str(user_data['account'])
        random_hash = Generate_random_hash()
        hashed = random_hash.generate()
        crop_hash=hashed[:10]
        user_data['verification']=crop_hash
        user = await add_user(user_data)
        token = await get_uid(user['email'], account)
        email_artifacts = dict(email=user_data['email'], name=user_data['firstname'], hash_code=crop_hash, account=account, token=token)

        # Send email as background task.
        create_notificaiton = Create_email_notification(email_artifacts)
        background_task.add_task(create_notificaiton.send_mail)
        return Create_account_response(status_code=200, token=str(token), detail=f"Successful! Account created.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Bad request - {e}')




@router.post("/login")
async def login(payload:Annotated[Login, Depends(user_login_method)]):
    return payload


@router.get("/verify-accout/{code}/{account}/{token}")
async def verify_account(code:str, account:str, token:str):
    instantiate_decryption=Encryption_handler(token, "password")
    uid = instantiate_decryption.decrypt()
    resp = await verify_accounts(dict(account=account, uid=uid, hash=code))
    return resp