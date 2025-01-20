
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

class Encryption_handler():
    def __init__(self, data:str, selector:str):
        self.data = data
        self.selector = selector
        self.key_store=dict(
            password=os.getenv('PSW_ENCRYPTION_KEY'), 
            token=os.getenv('TOKEN_KEY'))


    def encrypt(self):
        proceed_to = Fernet(self.key_store[self.selector].encode())
        return proceed_to.encrypt(str(self.data).encode())


    def decrypt(self):
        proceed_to = Fernet(self.key_store[self.selector].encode())
        raw_decryption = proceed_to.decrypt(self.data)
        return raw_decryption.decode()


class Generate_random_hash():
    def __init__(self):
        import hashlib
        import secrets
        self.hashlib = hashlib
        self.secrets = secrets

    def generate(self):
        random_token=self.secrets.token_hex(5)
        hash_object = self.hashlib.sha256(random_token.encode())
        generated_hash = hash_object.hexdigest()
        return generated_hash


    