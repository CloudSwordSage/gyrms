# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Enum, select
from sqlalchemy.sql import expression
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base

class User(Base):
    __tablename__ = "user"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    real_name = Column(String(50), nullable=False)
    role = Column(Enum('管理员', '护理主任', '护理工'), nullable=False)
    phone = Column(String(11), nullable=False)
    is_activate = Column(Boolean, server_default=expression.true())

    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str):
        result = await db.execute(
            select(cls).where(cls.username == username)
        )
        return result.scalars().first()

    @classmethod
    async def get_by_uid(cls, db: AsyncSession, uid: int):
        result = await db.execute(
            select(cls).where(cls.uid == uid)
        )
        return result.scalars().first()
