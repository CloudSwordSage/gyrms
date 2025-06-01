# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "管理员"
    director = "护理主任"
    worker = "护理工"

class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="用户名")
    real_name: str = Field(..., max_length=50, description="真实姓名")
    role: UserRole = Field(..., description="用户角色")
    phone: str = Field(..., max_length=11, description="手机号")
    is_activate: Optional[bool] = Field(True, description="是否激活")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255, description="密码")

class UserUpdate(BaseModel):
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    role: Optional[UserRole] = Field(None, description="用户角色")
    phone: Optional[str] = Field(None, max_length=11, description="手机号")
    is_activate: Optional[bool] = Field(None, description="是否激活")
    password: Optional[str] = Field(None, min_length=6, max_length=255, description="密码")

class UserInDB(UserBase):
    uid: int = Field(..., description="用户ID")

    class Config:
        from_attributes = True
