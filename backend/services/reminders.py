# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from models.reminder import Reminder
from sqlalchemy import select
from fastapi import HTTPException
from typing import List
from datetime import date

class ReminderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reminder(self, pid: int, reminder_type: str, cycle: str, next_reminder_date: date) -> Reminder:
        """创建新提醒"""
        reminder = Reminder(
            pid=pid,
            reminder_type=reminder_type,
            cycle=cycle,
            next_reminder_date=next_reminder_date
        )
        self.db.add(reminder)
        await self.db.flush()
        await self.db.refresh(reminder)
        return reminder

    async def get_reminders_by_pid(self, pid: int, page: int = 1, page_size: int = 10) -> List[Reminder]:
        """获取患者的所有提醒"""
        stmt = select(Reminder)\
            .where(Reminder.pid == pid)\
            .order_by(Reminder.next_reminder_date.asc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_reminder_cycle(self, reminder_id: int, cycle: str) -> Reminder:
        """更新提醒周期"""
        stmt = select(Reminder).where(Reminder.reminder_id == reminder_id)
        result = await self.db.execute(stmt)
        reminder = result.scalars().first()
        if not reminder:
            raise HTTPException(status_code=404, detail="提醒不存在")

        reminder.cycle = cycle
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    async def delete_reminder(self, reminder_id: int) -> None:
        """删除提醒"""
        stmt = select(Reminder).where(Reminder.reminder_id == reminder_id)
        result = await self.db.execute(stmt)
        reminder = result.scalars().first()
        if not reminder:
            raise HTTPException(status_code=404, detail="提醒不存在")

        await self.db.delete(reminder)
        await self.db.commit()
