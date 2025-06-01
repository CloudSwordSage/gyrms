# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReminderBase(BaseModel):
    pid: int
    reminder_type: str
    cycle: str
    next_reminder_date: date

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    reminder_id: int

    class Config:
        from_attributes = True

class ReminderUpdate(BaseModel):
    reminder_type: Optional[str] = None
    cycle: Optional[str] = None
    next_reminder_date: Optional[date] = None
