# -*- coding: utf-8 -*-
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from models.user import User
from utils.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from jose.exceptions import JWEError, ExpiredSignatureError

def rsa_decrypt(encrypted_data: str) -> str:
    """
    RSA解密函数
    :param encrypted_data: 加密的字符串
    :return: 解密后的原始字符串
    :raises: HTTPException 如果解密失败
    """
    try:
        # 加载私钥
        private_key = serialization.load_pem_private_key(
            settings.private_key.encode(),
            password=None,
            backend=default_backend()
        )

        # Base64解码加密数据
        encrypted_bytes = base64.b64decode(encrypted_data)

        # RSA解密
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.PKCS1v15()
        )

        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"解密失败: {str(e)}"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(uid: int, expires_delta: timedelta = None):
    """
    生成JWT token
    :param uid: 用户ID
    :param expires_delta: token过期时间
    :return: JWT token字符串
    """
    to_encode = {
        "sub": str(uid),
        "uid": uid
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.private_key,
        algorithm="RS256"
    )
    return encoded_jwt

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.public_key,
            algorithms=["RS256"]
        )
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get_by_uid(db, uid=int(uid))
    if user is None:
        raise credentials_exception
    return user

def verify_token_expiry(token: str) -> dict:
    """
    验证JWT token是否过期
    :param token: JWT token字符串
    :return: 包含验证结果的字典
    :raises: HTTPException 如果token无效
    """
    try:
        payload = jwt.decode(
            token,
            settings.public_key,
            algorithms=["RS256"]
        )
        return {
            "is_valid": True,
            "is_expired": False,
            "uid": payload.get("uid"),
            "exp": payload.get("exp")
        }
    except ExpiredSignatureError:
        return {
            "is_valid": False,
            "is_expired": True,
            "uid": None,
            "exp": None
        }
    except JWTError:
        return {
            "is_valid": False,
            "is_expired": False,
            "uid": None,
            "exp": None
        }

def check_role(required_role: str = None):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if required_role and current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源"
            )
        return current_user
    return role_checker

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户(已激活)"""
    if not current_user.is_activate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户未激活"
        )
    return current_user
