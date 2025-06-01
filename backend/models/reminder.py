# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 16:40:40
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : reminder.py
# @Desc    :


from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, Text, ForeignKey
from sqlalchemy.sql import expression
from datetime import date

from .base import Base


class Reminder(Base):
    __tablename__ = "reminder"

    reminder_id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("person.pid"), nullable=False)
    reminder_type = Column(String(50), nullable=False)
    cycle = Column(String(50), nullable=False)
    next_reminder_date = Column(Date, nullable=False)
