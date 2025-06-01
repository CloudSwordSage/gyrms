# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 16:36:59
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : care.py
# @Desc    :


from sqlalchemy import Column, Integer, Date, Text, ForeignKey, DateTime
from sqlalchemy.sql import expression
from datetime import datetime

from .base import Base

class Care(Base):
    __tablename__ = "care"

    care_id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("person.pid"), nullable=False)
    care_date = Column(Date, nullable=False)
    care_content = Column(Text, nullable=False)
    caregiver_id = Column(Integer, ForeignKey("user.uid"), nullable=False)
    evaluation = Column(Text, nullable=True)
    actual_time = Column(DateTime, nullable=True)
