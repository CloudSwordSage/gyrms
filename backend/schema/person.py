# -*- coding: utf-8 -*-
from pydantic import BaseModel, field_validator, StringConstraints
from datetime import date
from typing import Optional, Literal, Annotated, List

class PersonCreate(BaseModel):
    name: str
    gender: Literal['男', '女']
    age: int
    id_card: Annotated[str, StringConstraints(min_length=18, max_length=18)]
    phone: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    emergency_contact: str
    emergency_phone: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    bed_number: str
    category: Literal['孤寡老人', '残障人士', '短期托管']
    check_in_date: date
    photo: str

    @field_validator('id_card')
    def validate_id_card(cls, v):
        if not v[:-1].isdigit() or (v[-1].upper() not in ('X') and not v[-1].isdigit()):
            raise ValueError('无效身份证号')
        return v.upper()

    @field_validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('电话号码必须为数字')
        if not v.startswith(('1', '0')):
            raise ValueError('电话号码格式不正确')
        return v

    @field_validator('emergency_phone')
    def validate_emergency_phone(cls, v):
        if not v.isdigit():
            raise ValueError('紧急联系电话必须为数字')
        if not v.startswith(('1', '0')):
            raise ValueError('紧急联系电话格式不正确')
        return v

    @field_validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('年龄必须在0-120岁之间')
        return v

    @field_validator('bed_number')
    def validate_bed_number(cls, v):
        if not v:
            raise ValueError('床位号不能为空')
        if not any(char.isdigit() for char in v):
            raise ValueError('床位号必须包含数字')
        return v

class HealthBase(BaseModel):
    disease_history: Optional[str] = None
    allergy_history: Optional[str] = None
    blood_pressure: Optional[str] = None
    blood_glucose: Optional[float | str] = None
    last_checkup_date: Optional[date] = None
    medical_history: Optional[str] = None

class PersonQuery(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: str = "in"
    page: int = 1
    page_size: int = 20

class PersonID(BaseModel):
    pid: int

class PersonListItem(BaseModel):
    pid: int
    name: str
    gender: Literal['男', '女']
    age: int
    bed_number: str
    category: Literal['孤寡老人', '残障人士', '短期托管']
    check_in_date: date
    check_out_date: Optional[date] = None
    photo: str

class PersonListResponse(BaseModel):
    code: int = 200
    total: int
    items: list[PersonListItem]
    page: int
    page_size: int

class PersonDetail(BaseModel):
    pid: int
    name: str
    gender: Literal['男', '女']
    age: int
    id_card: str
    phone: str
    emergency_contact: str
    emergency_phone: str
    bed_number: str
    category: Literal['孤寡老人', '残障人士', '短期托管']
    check_in_date: date
    check_out_date: Optional[date] = None
    check_out_reason: Optional[str] = None
    photo: str

class Health(HealthBase):
    # health_id: int
    pid: int

class PersonDetailItem(BaseModel):
    person_data: PersonDetail
    health_data: Health

class PersonDetailResponse(BaseModel):
    code: int = 200
    data: PersonDetailItem

class PersonCreateResponse(BaseModel):
    code: int = 200
    message: str
    pid: int

class HealthCreate(HealthBase):
    pid: int

    class Config:
        from_attributes = True

class HealthUpdate(BaseModel):
    disease_history: Optional[str] = None
    allergy_history: Optional[str] = None
    blood_pressure: Optional[str] = None
    blood_glucose: Optional[str] = None
    last_checkup_date: Optional[date] = None
    medical_history: Optional[str] = None

class BedNumber(BaseModel):
    pid: int
    bed_number: str

class BedNumberResponse(BaseModel):
    code: int = 200
    total: int
    items: list[BedNumber]
    page: int
    page_size: int

class BedNumberQuery(BaseModel):
    page: int = 1
    page_size: int = 20
