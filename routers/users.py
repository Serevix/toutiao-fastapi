from fastapi import HTTPException

from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud.users import authenticate_user
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from crud import users
from utils.response import success_response
from utils.auth import get_current_user

router=APIRouter(prefix="/api/users",tags=["users"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    #验证用户是否存在-》创建用户-》生成token-》响应结果
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)
    # return {
    #     "code":200,
    #     "message":"success",
    #     "data":{
    #         "token":token,
    #         "userInfo":{
    #             "id":user.id,
    #             "username":user.username,
    #             "avatar":user.avatar,
    #             "bio":user.bio
    #         }
    #     }
    # }
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(msg="注册成功",data=response_data)

@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    user = await authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(msg="登录成功",data=response_data)

@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user)):
    return success_response(msg="获取用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,
                           user:User = Depends(get_current_user),
                           db:AsyncSession=Depends(get_db())):
    user=await users.update_user(db,user.username,user_data)
    return success_response(msg="更新用户信息成功",
                            data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(
        password_data:UserChangePasswordRequest,
        user:User = Depends(get_current_user),
        db:AsyncSession=Depends(get_db())):
    res_change_password=await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="旧密码错误")
    return success_response(msg="更新用户密码成功")






