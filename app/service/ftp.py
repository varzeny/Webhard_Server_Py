# service/ftp.py

# lib
from fastapi import FastAPI
import subprocess

# module


# define
class Manager:
    env:dict|None
    is_active:bool|None

    @classmethod
    def setup(cls, app:FastAPI):
        cls.env = app.state.env["app"]["service"]["ftp"]
    
    @classmethod
    def status(cls):
        result = subprocess.run(
            ["pgrep", "-x", "vsftpd"],
            capture_output=True,
            text=True
        )
        is_active = result.stdout.strip()
        if is_active == "active":
            cls.is_active = True
        else:
            cls.is_active = False
        return cls.is_active
        
    @classmethod
    def onoff(cls, onoff:bool):
        if cls.is_active == onoff:
            raise Exception("서버 상태가 제대로 전달되지 않고 있음")
        
        if onoff:
            result = subprocess.run(
                ["service", "vsftpd", "start"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        else:
            result = subprocess.run(
                ["service", "vsftpd", "stop"],
                capture_output=True,
                text=True
            )
            print(result.stdout)


    


# 서버 상태 확인

# 서버 키고 끄기

