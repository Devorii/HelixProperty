"""
Module Name: user_access.py
Description: Controls the flow of account information in an out of our database.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""


from fastapi import HTTPException
from database_ops.db_connection import get_db
from models.users import Owner, Tenants
from sqlalchemy import select, update, and_



user_account = {'OW1':Owner, 'TE1': Tenants}


async def verify_accounts(payload: dict) -> str:
    '''
    Manages the validation of user's accounts.

    :params dict:payload
    :return str
    '''
    try: 
        with get_db() as db:
            is_valid_query = select(user_account[payload['account']].verification).where(user_account[payload['account']].id == payload['uid'])
            is_valid=db.execute(is_valid_query).fetchone()
            db_validation_status=bool(is_valid[0])

            if not db_validation_status:
                operator = (
                        update(user_account[payload['account']])
                        .values(verification="True")  # Corrected typo
                        .where(and_(user_account[payload['account']].verification == payload['hash'],
                                    user_account[payload['account']].id == payload['uid'])))
                
                db.execute(operator)
                db.commit()
                return "Account Verified"
            return dict(status_code=200, detail="This account has been verified")
    except Exception as e:  
        raise HTTPException(status_code=400, detail=f"User not found or verification failed-{e}")




async def does_email_exist(user_email:str, account: str):
    '''
    Validates the persistence of the user's email

    :params str:user_email
    :params str:account

    :return bool
    '''
    try:
        with get_db() as db:
            find_email_query = select(user_account[account].email).where(user_account[account].email==user_email)
            exist=db.execute(find_email_query).fetchone()
            if not exist:
                return True
            else:
                return False
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)