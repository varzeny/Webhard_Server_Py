# jwt.py

# lib
import jwt
from datetime import datetime, timezone, timedelta


# define
def create_jwt(payload:dict, secret_key:str, algorithm:str, exp_min:float):
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=exp_min)
    encoded_token = jwt.encode(
        payload = payload,
        key = secret_key,
        algorithm = algorithm
    )
    return encoded_token


def verify_jwt(encoded_token:str, secret_key:str, algorithm:str):
    try:
        decoded_token = jwt.decode(
            jwt=encoded_token,
            key= secret_key,
            algorithms= algorithm
        )
        return decoded_token
    except jwt.ExpiredSignatureError as e:
        print("this Token has expired : ", e)
        return None
    except jwt.InvalidTokenError as e:
        print("this Token is Invalid token : ", e)
        return None
    except Exception as e:
        print("error from verify_token : ", e)
        return None  