"""
Author: Decory Herbert
"""

from fastapi import HTTPException
from database_ops.db_connection import get_db
from database_ops.models.db_models import Owner, Tenants
from encryption.handler import Encryption_handler
from sqlalchemy import select, update, and_, not_

user_account = {'OW1':Owner, 'TE1': Tenants}

async def add_user(user:dict):
    ''' Creates new user'''
    try:
        with get_db() as db:
            acc = user['account']
            user.pop('account', None)
            db.add(user_account[acc](**user))
            db.commit()
            return dict(email=user['email'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add user - {e}")

async def does_email_exist(user_email:str, account: str):
    '''Checks for email existence'''
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


async def get_uid(email:str, account:str):
    try: 
        with get_db() as db:
            operator = select(user_account[account].id).where(user_account[account].email == email)
            uid = db.execute(operator).fetchone()
            if uid is not None:
                user_id=uid[0]
                init_encryption = Encryption_handler(str(user_id), "password")
                token=init_encryption.encrypt()
            return token.decode()
    except Exception as e:  
        raise HTTPException(status_code=400, detail="user not found")


async def verify_accounts(payload: dict):
    '''Validate user's Hash'''
    try: 
        with get_db() as db:
            is_valid_query = select(user_account[payload['account']].verification).where(user_account[payload['account']].id == payload['uid'])
            is_valid=db.execute(is_valid_query).fetchone()
            db_validation_status = str(is_valid[0]) if is_valid[0] != "True" else bool(is_valid[0])
            print(db_validation_status, type(db_validation_status))
            
            if db_validation_status is True:
                return dict(status_code=200, detail="This account has been verified")
            else:
                operator = (
                        update(user_account[payload['account']])
                        .values(verification="True")  # Corrected typo
                        .where(
                            and_(
                                user_account[payload['account']].verification == payload['hash'],
                                user_account[payload['account']].id == payload['uid']
                            )
                        )
                    )
                    
                db.execute(operator)
                db.commit()
                return "Account Verified"
    except Exception as e:  
        raise HTTPException(status_code=400, detail=f"User not found or verification failed-{e}")


async def is_user(data:dict): 
    '''Validate the existence of a user.'''
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