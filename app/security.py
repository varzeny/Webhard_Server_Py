# core/security

# lib
from app.util import jwt as JWT
from secrets import token_hex

# module


# define
class Manager:
    # auth_server
    auth_url:str|None

    # access_token
    access_name:str|None
    access_secretkey:str|None
    access_algorithm:str|None
    access_expmin:float|None


    @classmethod
    def setup(cls, env:dict):
        # auth_server
        cls.auth_url=env["auth"]["url"]

        # access_token
        cls.access_name=env["access"]["name"]
        cls.access_secretkey=env["access"]["secretkey"]
        cls.access_algorithm=env["access"]["algorithm"]
        cls.access_expmin=env["access"]["expmin"]


    @classmethod
    def create_refresh_token(cls):
        return token_hex(64)


    @classmethod
    def create_access_token(cls, decoded_token:dict):
        encoded_token = JWT.create_jwt(
            payload=decoded_token,
            secret_key=cls.access_secretkey,
            algorithm=cls.access_algorithm,
            exp_min=cls.access_expmin
        )
        return encoded_token

    @classmethod
    def verify_access_token(cls, encoded_token:str):
        decoded_token = JWT.verify_jwt(
            encoded_token=encoded_token,
            secret_key=cls.access_secretkey,
            algorithm=cls.access_algorithm
        )
        return decoded_token
    