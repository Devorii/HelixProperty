"""
Module Name: login.py
Description: Manages user access to our application.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
    - cachetools >= 5.5.x
"""

from fastapi import HTTPException
from security.encryption.handler import Encryption_handler
from models.request import Login
from security.access_control.crud_db.user_access import is_user, get_user_initials
from dependencies.ttl_cache import CacheTool



async def user_login_method(user_data:Login) -> dict:
    '''
    Validates user's login information. 
    If account not verified kicks back error. 

    [ password ] in Encryption_handler refers to encryption .env value

    :param Login:user_data

    :return dict(status_code, token, user_initials)
    '''
    data=user_data.dict()
    user_info=await is_user(data)

    if user_info['verification'] != "True":
        raise HTTPException(status_code=409, detail="Almost there! Verify your account.")    
    else:
        decrypt_password = Encryption_handler(user_info['password'], "password")
        decrypted_password=decrypt_password.decrypt()


        if decrypted_password != data['password']:
            raise HTTPException(status_code=403, detail="Invalid password")
        else: 
            encrypt_token = Encryption_handler(user_info['id'], "password")
            generated_token=encrypt_token.encrypt()

            # Token should persist in cached.
            await CacheTool.set_cache(str(generated_token))
            user_data=await get_user_initials(user_data.email, user_data.account)
            return dict(status_code=200, token=generated_token, user_initials=user_data['initials'], name=user_data['name'],uid=user_info['id'], account=data['account'])