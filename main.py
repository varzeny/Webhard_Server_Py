# main

# lib
from dotenv import load_dotenv
from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# module
from app import Manager as APP
from app.middleware.access import Manager as ACCS_MW

# define
load_dotenv()
async def startup():
    APP.setup( app )
    return

async def shutdown():
    return


app = FastAPI()
app.state.env = {
    "project":{},
    "app":{
        "core":{},
        "service":{
            "access":{
                "secretkey":getenv("APP_SERVICE_ACCESS_SECRETKEY"),
                "algorithm":getenv("APP_SERVICE_ACCESS_ALGORITHM"),
                "expmin":getenv("APP_SERVICE_ACCESS_EXPMIN")
            },
            "ftp":{
                "ip":getenv("APP_SERVICE_FTP_IP"),
                "id":getenv("APP_SERVICE_FTP_ID"),
                "pw":getenv("APP_SERVICE_FTP_PW")
            }
        }
    }
}
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
# app.add_middleware(
#     middleware_class=CORSMiddleware,
#     allow_origins=["https://test.varzeny.com", "https://test2.varzeny.com"],  # 각 서비스 및 인증 서버 도메인 모두 추가
#     allow_credentials=True,  # 쿠키 전송 허용
#     allow_methods=["*"],  # 모든 메서드 허용
#     allow_headers=["*"],  # 모든 헤더 허용
# )
app.add_middleware( ACCS_MW )


# script
if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=9010,
        workers=1,
        reload=True
    )