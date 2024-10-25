# access.py

# lib
from fastapi import FastAPI

# module
from ..core.util import jwt

# define
class Manager:
    env:dict|None

    @classmethod
    def setup(cls, app:FastAPI):
        # env
        cls.env = app.state.env["app"]["service"]["access"]


    @classmethod
    def decoding_token(cls, encoded_token:str):
        decoded_token = jwt.verify_jwt(
            encoded_token=encoded_token,
            secret_key=cls.env.get("secretkey"),
            algorithm=cls.env.get("algorithm")
        )
        if decoded_token:
            return decoded_token
        else:
            return None