# app/__init__.py

# lib
from fastapi import FastAPI, staticfiles

# module
from .api.endpoint import router
from .service.access import Manager as ACCS

# define
class Manager:
    env:dict|None

    @classmethod
    def setup(cls, app:FastAPI):
        # env
        cls.env = app.state.env["app"]

        # api
        app.include_router( router )

        # mount
        app.mount(
            path="/static",
            app=staticfiles.StaticFiles(directory="app/core/static"),
            name="static"
        )

        # core
        ## database

        # service
        ACCS.setup(app)
