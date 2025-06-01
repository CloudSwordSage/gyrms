# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class CareBase(BaseModel):
    pid: int
    caregiver_id: int
    care_content: str
    care_date: date
    evaluation: Optional[str] = None
    actual_time: Optional[datetime] = None

class CareCreate(CareBase):
    care_type: str

class Care(CareBase):
    care_id: int
    actual_time: datetime

    class Config:
        from_attributes = True

class CareUpdate(BaseModel):
    care_content: Optional[str] = None
    care_date: Optional[date] = None
    evaluation: Optional[str] = None

class PageCareResponse(BaseModel):
    total: int
    items: list[Care]

class PageParams(BaseModel):
    page: int = 1
    page_size: int = 10
