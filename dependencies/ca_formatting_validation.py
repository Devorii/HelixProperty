
import re
from fastapi import HTTPException
from security.encryption.handler import Encryption_handler
from security.access_control.crud_db.account_access import does_email_exist
# from models.request import Create_user_request




async def payload_validation(data: dict):
    '''VALIDATES EMAIL FORMATTING'''

    # EMAIL PATTERN TO MATCH
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    phone_pattern = r'^\d{3}-?\d{3}-?\d{4}$'


    if re.match(email_pattern, data['email']) and re.match(phone_pattern, data['phone']):
        # DOES THE EMAIL EXIST?
        existing=await does_email_exist(data['email'], data['account'])
        if not existing:
            raise HTTPException(status_code=409, detail="There is already an account with this email.")
        else:
            password_handler = Encryption_handler(data['password'], "password")
            encrypted_password = password_handler.encrypt()
            data['password']=encrypted_password
            return data
 
    else:
        raise HTTPException(status_code=422, detail="Invalid email or phone formatting")
 