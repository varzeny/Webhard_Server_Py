# api/endpoint.py

# lib
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, FileResponse


# module
from ..service.access import Manager as ACCS
from ..service.ftp import Manager as FTP


# define
router = APIRouter()
template = Jinja2Templates(directory="app/core/template")


# dependency
async def guest_only(req:Request):
    if req.state.access_token.get("role") == "guest":
        return req.state.access_token
    else:
        raise HTTPException(status_code=401, detail="you are not guest")

async def user_only(req:Request):
    if req.state.access_token.get("role") != "guest":
        return req.state.access_token
    else:
        raise HTTPException(status_code=401, detail="you are not user")
    
async def admin_only(req:Request):
    if req.state.access_token.get("role") == "admin":
        return req.state.access_token
    else:
        raise HTTPException(status_code=401, detail="you are not admin")


# endpoint
@router.get("/")
async def get_root(req:Request):

    t = req.state.access_token
    print(t)

    resp = template.TemplateResponse(
        request=req,
        name="files.html",
        context={
            "role":t.get("role")
        },
        status_code=200
    )
    return resp

# files #############################################################
@router.get("/files")
async def get_files(req:Request):
    try:
        t = req.state.access_token
        print(t)

        resp = template.TemplateResponse(
            request=req,
            name="files.html",
            context={
                "role":t.get("role")
            },
            status_code=200
        )
        return resp

    except Exception as e:
        print("ERROR from get_files : ", e)
        return Response(status_code=400)


@router.get("/files/search/{name:path}")
async def get_file_list(req:Request,name:str):
    try:
        print("요청받은 파일 : ", name)
        base_path = "./files"
        if name=="root":
            path=base_path
        else:
            path=os.path.join(base_path, name)

        # 경로 유효성 확인
        if not os.path.isdir(path):
            return Response(content="Invalid directory path", status_code=400)
        

        # 파일목록
        dir_list = []
        file_list = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                file_list.append(item)
            else:
                dir_list.append(item)
        # print("dir_list",dir_list)        
        # print("file_list",file_list)

        return JSONResponse(
            content={
                "dir_list":dir_list,
                "file_list":file_list
            },
            status_code=200
        )

    except Exception as e:
        print("ERROR from get_file_list : ", e)
        return Response(status_code=400)


@router.get("/files/download/{name:path}")
async def get_download_file(req:Request, name:str):
    try:
        base_path = "./files"
        file_path = os.path.join(base_path, name)

        # 파일 존재 여부 확인
        if not os.path.isfile(file_path):
            return HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/octet-stream"
        )

    except Exception as e:
        print("ERROR from get_download_file : ", e)
        return Response(status_code=400)
    

# FTP #############################################################
@router.get("/ftp/page")
async def get_ftp_page(req:Request, t=Depends(admin_only)):
    try:
        print(t)

        resp = template.TemplateResponse(
            request=req,
            name="ftp.html",
            context={
                "role":t.get("role")
            },
            status_code=200
        )
        return resp
    
    except Exception as e:
        print("ERROR from get_ftp_page : ", e)
        return Response(status_code=400)


@router.get("/ftp/status")
async def get_status(req:Request):
    try:
        print("FTP 서버 상태 확인 요청 받음")
        onoff = FTP.status()

        return JSONResponse(status_code=200, content={"onoff":onoff})
    except Exception as e:
        print("ERROr from get_status : ", e)
        return Response(status_code=400)


@router.post("/ftp/onoff")
async def post_onoff(req:Request):
    try:
        print("서버 상태 변경 요청 받음 !")
        reqData = await req.form()
        print("----------------onoff : ",reqData)

        print()

        return Response(status_code=200)
    except Exception as e:
        print("ERROR from post_onoff : ", e)
        return Response(status_code=400)
    

@router.post("/ftp/test")
async def post_test(req:Request):
    try:
        reqData = await req.json()
        print(reqData)
        return Response(status_code=200)
    except Exception as e:
        print("ERROR from post_test :", e)
        return Response(status_code=400)