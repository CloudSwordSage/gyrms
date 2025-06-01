# -*- coding: utf-8 -*-
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from models.user import User
from schema.auth import Token, LoginRequest, TokenVerificationResult, VerifyTokenRequest, UserInfo
from utils.database import get_db
from utils.security import verify_password, create_access_token, rsa_decrypt, verify_token_expiry, get_current_user
from config.config import settings

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    # 查询用户
    user = await User.get_by_username(db, login_data.username)
    try:
        decrypted_password = rsa_decrypt(login_data.password)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码解密失败"
        )

    if not user or not verify_password(decrypted_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        uid=user.uid,
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/public_key")
async def get_public_key():
    return {
        "code": 200,
        "data": settings.public_key,
        "message": "成功"
    }

@router.post("/verify_token", response_model=TokenVerificationResult)
async def verify_token(request: VerifyTokenRequest):
    """
    验证JWT token是否有效及是否过期
    :param request: 包含token的请求体
    :return: Token验证结果
    """
    return verify_token_expiry(request.token)

@router.get("/me", response_model=UserInfo)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的基础信息
    :return: 包含username, role, phone的用户信息
    """
    return {
        "uid": current_user.uid,
        "username": current_user.username,
        "role": current_user.role,
        "phone": current_user.phone
    }
