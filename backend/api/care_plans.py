# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.care_plan import CarePlan
from schema.care_plan import (
    CarePlan,
    CarePlanCreate,
    CarePlanAccept,
    CarePlanTransfer,
    CarePlanAssign,
    CarePlanComplete,
    AvailableResponse
)
from services.care_plans import CarePlanService
from utils.database import get_db
from utils.security import get_current_user

router = APIRouter(prefix="/care_plan", tags=['护理计划'])

@router.get("/detail/{plan_id}", response_model=CarePlan)
async def get_care_plan_detail(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """获取护理计划详情"""
    service = CarePlanService(db)
    return await service.get_plan_by_id(plan_id)

@router.post("/", response_model=CarePlan)
async def create_care_plan(
    plan_data: CarePlanCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建护理计划(管理员/护理主任)"""
    if current_user.role not in ["管理员", "护理主任"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员/护理主任可以创建护理计划"
        )
    service = CarePlanService(db)
    return await service.create_care_plan(plan_data)

@router.get("/available", response_model=AvailableResponse)
async def get_available_plans(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取可接取的任务列表"""
    service = CarePlanService(db)
    return await service.get_available_plans(page=page, page_size=page_size)

@router.post("/{plan_id}/accept", response_model=CarePlan)
async def accept_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """接取护理任务"""
    service = CarePlanService(db)
    return await service.accept_plan(plan_id, current_user.uid)

@router.post("/{plan_id}/abandon", response_model=CarePlan)
async def abandon_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """放弃护理任务"""
    service = CarePlanService(db)
    return await service.abandon_plan(plan_id, current_user.uid)

@router.post("/{plan_id}/transfer", response_model=CarePlan)
async def transfer_plan(
    plan_id: int,
    transfer_data: CarePlanTransfer,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """转交护理任务"""
    service = CarePlanService(db)
    return await service.transfer_plan(
        plan_id,
        current_user.uid,
        transfer_data.new_executor_id
    )

@router.post("/{plan_id}/assign", response_model=CarePlan)
async def assign_plan(
    plan_id: int,
    assign_data: CarePlanAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """分配护理任务(管理员/护理主任)"""
    if current_user.role not in ["管理员", "护理主任"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权进行任务分配"
        )
    service = CarePlanService(db)
    return await service.assign_task(
        plan_id,
        assign_data.executor_id,
        assign_data.assign_type
    )

@router.get("/my", response_model=AvailableResponse)
async def get_my_plans(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户的护理计划"""
    service = CarePlanService(db)
    return await service.get_my_plans(current_user.uid, page=page, page_size=page_size)

@router.get("/all", response_model=AvailableResponse)
async def get_all_plans(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """获取所有护理计划(管理员/护理主任)"""
    service = CarePlanService(db)
    return await service.get_all_plans(page=page, page_size=page_size)

@router.post("/{plan_id}/complete", response_model=CarePlan)
async def complete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """完成护理计划"""
    service = CarePlanService(db)
    return await service.complete_plan(plan_id, current_user.uid)
