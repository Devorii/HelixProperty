"""
Module Name: session_control.py
Description: Used as a dependency for our session validation.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - cachetools >= 5.5.x
"""

from fastapi import HTTPException, Header
from security.encryption.handler import Encryption_handler
from dependencies.ttl_cache import CacheTool

# def validate_user_account(user:dict) -> dict:
async def validate_user_account(x_access_token:str=Header(None)) -> dict:
    '''
    Ensures user existance and converts user token to uid.
    
    :params dict:user

    :return dict: user
    '''
    # token=user['token']
    if not x_access_token:
        raise HTTPException(status_code=403, detail='Unauthorized access. Token is missing')
    
    # Is token in Cache?
    is_valid=await CacheTool.get_cache(x_access_token.encode('utf-8'))
    if not is_valid:
        raise HTTPException(status_code=403, detail='Session expired')

    # # # Decode token
    instantiate_encryptor = Encryption_handler(x_access_token, "password")
    uid=int(instantiate_encryptor.decrypt())
  
    return uid
