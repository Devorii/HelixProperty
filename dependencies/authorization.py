from fastapi import HTTPException
from encryption.handler import Encryption_handler
from models.request import Login
from database_ops.crud.admin import is_user

def validate_user_account(user:dict):
    '''CONVERTS USER TOKEN TO ID'''
    token=user['token']
    if not token:
        raise HTTPException(status_code=403, detail='Unauthorized access. Token is missing')
    else:
        # Decode token
        instantiate_ecryptor = Encryption_handler(token, "password")
        uid=Encryption_handler.decrypt()
        user['token']=uid
        return user
    
async def user_login_method(user_data:Login):
    data=user_data.dict()
    # IS THERE SOME AN ASSOCIATED ACCOUNT
    raw_db_data=await is_user(data)
    if raw_db_data['verification'] != "True":
        raise HTTPException(status_code=409, detail="Almost there! Verify your account.")    
    else:
        decrypt_password = Encryption_handler(raw_db_data['password'], "password")
        decrypted_password=decrypt_password.decrypt()
        encrypt_token = Encryption_handler(raw_db_data['id'], "password")
        if decrypted_password != data['password']:
            raise HTTPException(status_code=403, detail="Invalid password")
        else: 
            generated_token=encrypt_token.encrypt()
            return dict(status_code=200,  token=generated_token)




    # IS THE ACCOUNT VERIFIED
    # MATCH PASSWORD


