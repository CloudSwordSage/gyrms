# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.reminder import Reminder
from schema.reminder import Reminder, ReminderCreate, ReminderUpdate
from services.reminders import ReminderService
from utils.database import get_db
from utils.security import get_current_user

router = APIRouter(prefix="/reminder", tags=["提醒"])

@router.post("/", response_model=Reminder)
async def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新提醒"""
    service = ReminderService(db)
    return service.create_reminder(
        pid=reminder.pid,
        reminder_type=reminder.reminder_type,
        cycle=reminder.cycle,
        next_reminder_date=reminder.next_reminder_date
    )

@router.get("/{pid}", response_model=List[Reminder])
async def get_reminders(
    pid: int,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取患者的所有提醒"""
    service = ReminderService(db)
    return service.get_reminders_by_pid(pid, page=page, page_size=page_size)

@router.put("/{id}", response_model=Reminder)
async def update_reminder(
    id: int,
    update_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新提醒"""
    service = ReminderService(db)

    if update_data.cycle:
        return service.update_reminder_cycle(id, update_data.cycle)

    # 可以扩展其他更新逻辑
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="仅支持更新周期"
    )

@router.delete("/{id}")
async def delete_reminder(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除提醒"""
    service = ReminderService(db)
    service.delete_reminder(id)
    return {"message": "提醒已删除"}
