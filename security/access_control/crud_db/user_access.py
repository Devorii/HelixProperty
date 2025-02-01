"""
Module Name: user_access.py
Description: Controls the flow of user information in an out of our database.

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
from security.encryption.handler import Encryption_handler
from sqlalchemy import select


user_account = {'OW1':Owner, 'TE1': Tenants}

async def add_user(user:dict) -> dict:
    ''' 
    Stores user's information in our database.

    :params dict:user

    :return dict(email)
    '''
    try:
        with get_db() as db:
            acc = user['account']
            user.pop('account', None)
            user.pop('propCodeMngmt', None)
            db.add(user_account[acc](**user))
            db.commit()
            return dict(email=user['email'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")
    


async def get_uid(email:str, account:str):
    '''
    Finds user[id] from injected dependencies and 
    encrypts into a token

    :params str:email
    :params str:account -> 'OW1' or 'TE1'

    :return str: token.decode()
    '''
    try: 
        with get_db() as db:
            operator = select(user_account[account].id).where(user_account[account].email == email)
            uid = db.execute(operator).fetchone()
            if uid is not None:
                user_id=uid[0]
                init_encryption = Encryption_handler(str(user_id), "password")
                token=init_encryption.encrypt()
            return dict(uid=uid[0], token=token.decode())
    except Exception as e:  
        raise HTTPException(status_code=400, detail="user not found")




async def get_user_initials(email:str,account:str) -> dict:
    '''
    User injected dependencies email and account, 
    finds user's first and last name, extract the begining
    character to create thier initials. 

    :params str:email
    :params str:account 

    :return dict(initials)
    '''
    try: 
        with get_db() as db:
            operator = select(user_account[account].firstname, user_account[account].lastname ).where(user_account[account].email == email)
            user_init = db.execute(operator).fetchall()
            if user_init is not None:
                response=user_init[0]
                initials=str(response[0][0])+str(response[1][0])
        return dict(initials=initials, name=f'{response[0]} {response[1]}')
    except Exception as e:  
        raise HTTPException(status_code=400, detail=f"e: {e}")
    

async def is_user(data:dict): 
    '''
    Validate the existence of a user.

    :params dict: data
    :return dict(id, firstname, password, verification)
    '''
    try: 
        with get_db() as db:
            find_user_query = select(user_account[data['account']]).where(user_account[data['account']].email == data['email'])
            response = db.execute(find_user_query).fetchone()
            if not response: 
                raise HTTPException(status_code=400, detail="No account associated with this email")
            user_db_obj = response[0]
            return dict(id=user_db_obj.id, firstname=user_db_obj.firstname, password=user_db_obj.password, verification=user_db_obj.verification)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")