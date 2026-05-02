"""
用户相关的操作
"""
import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security


#根据用户名进行查询
async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db:AsyncSession,user_date:UserRequest):
    #先密码加密
    hashed_password=security.get_hash_password(user_date.password)
    user=User(username=user_date.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#从数据库读回最新的 user
    return user


#生成token
async def create_token(db:AsyncSession,user_id:int):
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=1,hours=2,minutes=30,seconds=60)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()

    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token

