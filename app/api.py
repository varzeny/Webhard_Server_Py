# api.py

# lib
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, FileResponse


# module
from app.security import Manager as SECURITY


# define
router = APIRouter()
template = Jinja2Templates(directory="app/template")


# dependency
async def guest_only(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    access_dt = SECURITY.verify_access_token(access_et)
    if access_et and access_dt:
        print("게스트 아님")
        raise HTTPException(status_code=401, detail="you are not guest")
    else:
        print("게스트 맞음")
        return access_dt

async def user_only(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    access_dt = SECURITY.verify_access_token(access_et)
    if access_et and access_dt:
        print("유저임")
        return access_dt
    else:
        print("access_token 없음")
        raise HTTPException(status_code=401, detail="access_token doesn't exist")
    
async def admin_only(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    access_dt = SECURITY.verify_access_token(access_et)
    if access_et and access_dt:
        print(access_dt)
        if access_dt.get("role_id")==1:
            print("관리자임")
            return access_dt
        else:
            print("엑세스 토큰은 있는데, 관리자가 아님")
            raise HTTPException(status_code=403, detail="you are not admin")
    else:
        print("access_token 없음")
        raise HTTPException(status_code=401, detail="access_token doesn't exist")


# endpoint
@router.get("/")
async def get_root(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    access_dt = SECURITY.verify_access_token(access_et)

    resp = template.TemplateResponse(
        request=req,
        name="files.html",
        context={
            "role_id":access_dt.get("role_id") if access_dt is not None else None
        },
        status_code=200
    )
    return resp

# files #############################################################
@router.get("/files")
async def get_files(req:Request):
    try:
        access_et = req.cookies.get(SECURITY.access_name)
        access_dt = SECURITY.verify_access_token(access_et)

        resp = template.TemplateResponse(
            request=req,
            name="files.html",
            context={
                "role_id":access_dt.get("role_id") if access_dt is not None else None
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
# @router.get("/ftp/page")
# async def get_ftp_page(req:Request, t=Depends(admin_only)):
#     try:
#         print(t)

#         resp = template.TemplateResponse(
#             request=req,
#             name="ftp.html",
#             context={
#                 "role":t.get("role")
#             },
#             status_code=200
#         )
#         return resp
    
#     except Exception as e:
#         print("ERROR from get_ftp_page : ", e)
#         return Response(status_code=400)


# @router.get("/ftp/status")
# async def get_status(req:Request):
#     try:
#         print("FTP 서버 상태 확인 요청 받음")
#         onoff = FTP.status()

#         return JSONResponse(status_code=200, content={"onoff":onoff})
#     except Exception as e:
#         print("ERROr from get_status : ", e)
#         return Response(status_code=400)


# @router.post("/ftp/onoff")
# async def post_onoff(req:Request):
#     try:
#         print("서버 상태 변경 요청 받음 !")
#         reqData = await req.form()
#         print("----------------onoff : ",reqData)

#         print()

#         return Response(status_code=200)
#     except Exception as e:
#         print("ERROR from post_onoff : ", e)
#         return Response(status_code=400)
    

# @router.post("/ftp/test")
# async def post_test(req:Request):
#     try:
#         reqData = await req.json()
#         print(reqData)
#         return Response(status_code=200)
#     except Exception as e:
#         print("ERROR from post_test :", e)
#         return Response(status_code=400)