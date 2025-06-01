# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.user import User
from schema.user import UserCreate, UserUpdate, UserInDB
from services.users import UserService
from utils.database import get_db
from utils.security import get_current_active_user

router = APIRouter(prefix="/user", tags=["用户"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 只有管理员可以创建用户
    if current_user.role != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以创建用户"
        )
    return await UserService.create_user(db, user_data)

@router.get("/", response_model=List[UserInDB])
async def get_users(
    username: str = "",
    name: str = "",
    role: str = "",
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 只有管理员可以查看用户列表
    if current_user.role != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看用户列表"
        )
    return await UserService.get_users(db, skip=skip, limit=limit, username=username, name=name, role=role)

@router.get("/{uid}", response_model=UserInDB)
async def get_user(
    uid: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 用户只能查看自己的信息，管理员可以查看所有用户
    if current_user.uid != uid and current_user.role != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看该用户信息"
        )
    user = await UserService.get_user(db, uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@router.put("/{uid}", response_model=UserInDB)
async def update_user(
    uid: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 用户只能更新自己的信息，管理员可以更新所有用户
    if current_user.uid != uid and current_user.role != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新该用户信息"
        )
    user = await UserService.update_user(db, uid, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    uid: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 只有管理员可以删除用户
    if current_user.role != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除用户"
        )
    if not await UserService.delete_user(db, uid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
