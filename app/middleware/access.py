# middleware/access.py

# lib
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import Response

# module
from app.service.access import Manager as ACCS

# define
class Manager(BaseHTTPMiddleware):
    async def dispatch(self, req:Request, call_next):
        # 전처리
        encodede_token = req.cookies.get("access_token")
        # print(encodede_token)
        decoded_token = ACCS.decoding_token(encodede_token)
        print("auth 에서 받은 토큰",decoded_token)
        req.state.access_token = decoded_token


        # 처리
        resp:Response = await call_next(req)

        # 후처리
        return resp