# main

# lib
from dotenv import load_dotenv
from os import getenv
from fastapi import FastAPI, staticfiles

# module
from app.security import Manager as SECURITY
from app import api as API

# define
load_dotenv()
async def startup():
    # security
    SECURITY.setup( app.state.env["app"]["security"] )

    # api
    app.include_router(API.router)


async def shutdown():
    return


app = FastAPI()
app.state.env = {
    "project":{
        "name":getenv("PROJECT_NAME"),
    },
    "app":{
        "security":{
            "auth":{
                "url":getenv("APP_SECURITY_AUTH_URL"),
            },
            "access":{
                "name":getenv("APP_SECURITY_ACCESS_NAME"),
                "secretkey":getenv("APP_SECURITY_ACCESS_SECRETKEY"),
                "algorithm":getenv("APP_SECURITY_ACCESS_ALGORITHM"),
                "expmin":int(getenv("APP_SECURITY_ACCESS_EXPMIN")),
            },
        },
    }
}
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="app/static"),
    name="static"
)

