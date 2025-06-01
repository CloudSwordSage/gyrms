# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 16:33:46
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : health.py
# @Desc    :


from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, Text, ForeignKey
from sqlalchemy.sql import expression
from datetime import date

from .base import Base


class Health(Base):
    __tablename__ = "health"

    health_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    pid = Column(Integer, ForeignKey("person.pid"), nullable=False)
    disease_history = Column(Text, nullable=True)
    allergy_history = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    last_checkup_date = Column(Date, nullable=True)
    blood_pressure = Column(String(20), nullable=True)
    blood_glucose = Column(String(20), nullable=True)
