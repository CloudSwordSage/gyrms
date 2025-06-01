# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.care import Care
from models.user import User
from schema.care import Care, CareCreate, CareUpdate, PageCareResponse, PageParams
from services.care import CareService
from utils.database import get_db
from utils.security import get_current_user

router = APIRouter(prefix="/care", tags=['护理记录'])

@router.post("/", response_model=Care)
async def create_care_record(
    care_data: CareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建护理记录"""
    service = CareService(db)
    care_content = f"{care_data.care_type} <||> {care_data.care_content}"
    return await service.create_care_record(
        pid=care_data.pid,
        caregiver_id=current_user.uid,
        care_content=care_content,
        care_date=care_data.care_date,
        evaluation=care_data.evaluation
    )

@router.get("/patient/{pid}", response_model=PageCareResponse)
async def get_care_records_by_patient(
    pid: int,
    query: PageParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取患者的护理记录"""
    service = CareService(db)
    return await service.get_care_records_by_patient(pid = pid, page=query.page, page_size=query.page_size)

@router.get("/caregiver/{caregiver_id}", response_model=PageCareResponse)
async def get_care_records_by_caregiver(
    caregiver_id: int,
    query: PageParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取护理员的护理记录"""
    service = CareService(db)
    return await service.get_care_records_by_caregiver(caregiver_id=caregiver_id, page=query.page, page_size=query.page_size)

@router.get("/detail/{care_id}", response_model=Care)
async def get_care_record_detail(
    care_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取护理记录详情"""
    service = CareService(db)
    return await service.get_care_record_detail(care_id=care_id)

@router.put("/{id}", response_model=Care)
async def update_care_record(
    id: int,
    update_data: CareUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新护理记录"""
    service = CareService(db)
    if not any([update_data.care_content, update_data.care_date, update_data.evaluation is not None]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供至少一个更新字段"
        )
    return await service.update_care_record(
        record_id=id,
        care_content=update_data.care_content,
        care_date=update_data.care_date,
        evaluation=update_data.evaluation
    )

@router.delete("/{id}")
async def delete_care_record(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除护理记录"""
    service = CareService(db)
    await service.delete_care_record(id)
    return {"message": "护理记录已删除"}
