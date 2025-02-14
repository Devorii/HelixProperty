import firebase_admin
from firebase_admin import credentials, storage
import base64
import json
import os
from dotenv import load_dotenv


load_dotenv()

STORAGE_BUCKET=os.getenv('STORAGEBUCKET')
FIREBASE_CERTIFICATE=os.getenv('FIREBASE_CREDS')
async def firebase_initializer(app):
    '''
    Initializes firebase credentials.
    '''
    decode_creds=base64.b64decode(FIREBASE_CERTIFICATE).decode("utf-8")
    cred_dict=json.loads(decode_creds)

    cred = credentials.Certificate(cred_dict)
    default_app=firebase_admin.initialize_app(cred, {'storageBucket': STORAGE_BUCKET})
    app.state.bucket=storage.bucket()