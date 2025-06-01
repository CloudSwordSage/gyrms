# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class PlanStatus(str, Enum):
    in_progress = "进行中"
    completed = "已结束"
    paused = "暂停"

class AssignType(str, Enum):
    voluntary = "自主接取"
    assigned = "强制分配"

class CarePlanBase(BaseModel):
    pid: int
    plan_name: str
    plan_content: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None

class CarePlanCreate(CarePlanBase):
    status: PlanStatus = Field(default="进行中")

class CarePlan(CarePlanBase):
    plan_id: int
    executor_id: Optional[int] = None
    status: PlanStatus

    class Config:
        from_attributes = True

class CarePlanAccept(BaseModel):
    executor_id: int

class CarePlanTransfer(BaseModel):
    new_executor_id: int

class CarePlanAssign(BaseModel):
    executor_id: int
    assign_type: AssignType

class CarePlanComplete(BaseModel):
    executor_id: int

class AvailableResponse(BaseModel):
    total: int
    items: list[CarePlan]
