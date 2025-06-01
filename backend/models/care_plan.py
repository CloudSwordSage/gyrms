# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 16:38:55
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : care_plan.py
# @Desc    :


from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, Text, ForeignKey
from sqlalchemy.sql import expression
from datetime import date

from .base import Base

class CarePlan(Base):
    __tablename__ = "care_plan"

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("person.pid"), nullable=False)
    executor_id = Column(Integer, ForeignKey("user.uid"), nullable=True)
    plan_content = Column(Text, nullable=False)
    frequency = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    plan_name = Column(String(100), nullable=False)
    status = Column(Enum('进行中', '已结束', '暂停', name='status_enum'), server_default='进行中', nullable=False)
