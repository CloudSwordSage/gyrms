# -*- coding: utf-8 -*-
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.user import User
from schema.user import UserCreate, UserUpdate, UserInDB
from utils.security import get_password_hash
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> UserInDB:
        # 检查用户名是否已存在
        existing_user = await User.get_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            password=hashed_password,
            real_name=user_data.real_name,
            role=user_data.role.value,
            phone=user_data.phone,
            is_activate=user_data.is_activate
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return UserInDB.model_validate(user)

    @staticmethod
    async def get_user(db: AsyncSession, uid: int) -> Optional[UserInDB]:
        user = await User.get_by_uid(db, uid)

        if not user:
            return None
        return UserInDB.model_validate(user)

    @staticmethod
    async def update_user(
        db: AsyncSession,
        uid: int,
        user_data: UserUpdate
    ) -> Optional[UserInDB]:
        # 获取现有用户
        user = await User.get_by_uid(db, uid)
        if not user:
            return None

        # 更新字段
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
        if "role" in update_data:
            update_data["role"] = update_data["role"].value

        await db.execute(
            update(User)
            .where(User.uid == uid)
            .values(**update_data)
        )
        await db.commit()

        # 返回更新后的用户
        updated_user = await User.get_by_uid(db, uid)
        return UserInDB.model_validate(updated_user) if updated_user else None

    @staticmethod
    async def delete_user(db: AsyncSession, uid: int) -> bool:
        result = await db.execute(
            delete(User)
            .where(User.uid == uid)
        )
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        username: str = "",
        name: str = "",
        role: str = ""
    ) -> list[UserInDB]:
        stmt = select(User)
        if username:
            stmt = stmt.where(User.username.like(f"%{username}%"))
        if name:
            stmt = stmt.where(User.real_name.like(f"%{name}%"))
        if role:
            stmt = stmt.where(User.role == role)
        result = await db.execute(stmt)
        users = result.scalars().all()
        return [UserInDB.model_validate(user) for user in users]
