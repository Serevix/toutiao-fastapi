from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username:str=Field(...,min_length=2,max_length=20)
    password:str=Field(...,min_length=2,max_length=72)


#user_info 对应的类：基础类+Info类(id，用户名)
class UserInfoBase(BaseModel):
    """
    用户信息继承数据结构
    """
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像")
    gender:Optional[str]=Field("male",max_length=10,description="性别")
    bio:Optional[ str]=Field(None,max_length=500,description="简介")

class UserInfoResponse(UserInfoBase):
    id:int
    username:str
    #模型配置
    model_config = ConfigDict(
        from_attributes=True# 允许从ORM对象属性中获取值
    )

class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field( ..., description="用户信息",validation_alias="userInfo",serialization_alias="userInfo")
    model_config = ConfigDict(
        populate_by_name=True,#alias/字段名兼容
        from_attributes=True# 允许从ORM对象属性中获取值
    )
