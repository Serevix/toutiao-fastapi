from datetime import datetime
from typing import Optional

from sqlalchemy import Index,Integer,String,Enum,DateTime,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="user"
    __table_args__=(
        Index("username_UNIQUE", "username"),
        Index("phone_UNIQUE", "phone"),
    )
    id:Mapped[int]= mapped_column(Integer,primary_key=True,autoincrement=True,comment="用户ID")
    username:Mapped[str]=mapped_column(String(50),unique= True,nullable=False,comment="用户名")
    password:Mapped[str]=mapped_column(String(255),nullable=False,comment="密码(加密存储）")
    nickname:Mapped[Optional[str]]=mapped_column(String(50),comment="昵称")
    avatar:Mapped[Optional[str]]=mapped_column(String(255),comment="用户头像")
    gender:Mapped[str]=mapped_column(Enum('male','female','unknown'),comment="性别",default="unknown")
    bio:Mapped[Optional[str]]=mapped_column(String(255),comment="简介",default="这个人很懒")
    phone:Mapped[Optional[str]]=mapped_column(String(11),unique= True,comment="手机号")
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class UserToken(Base):
    __tablename__="user_token"
    __table_args__=(
        Index("token_UNIQUE", "token"),
        Index("fk_user_token_user_idx", "user_id"),
    )

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="用户ID")
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("user.id"),nullable=False,comment="用户ID")
    token:Mapped[str]=mapped_column(String(255),unique= True,nullable=False,comment="用户Token")
    expires_at:Mapped[datetime]=mapped_column(DateTime, nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now(),comment="创建时间")
    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token})>"
    