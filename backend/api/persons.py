# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Optional

from utils.database import get_db
from utils.security import get_current_user, check_role
from models.user import User
from services.persons import PersonService
from services.persons import HealthService
from schema.person import (
    PersonCreate,
    PersonQuery,
    PersonID,
    PersonListResponse,
    PersonDetailResponse,
    PersonCreateResponse,
    HealthBase,
    BedNumberResponse,
    BedNumberQuery
)
router = APIRouter(prefix="/persons", tags=["人员"])

@router.get("/get_bed_number", response_model=BedNumberResponse)
async def get_bed_number(
    query: BedNumberQuery = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """获取床位号列表"""
    try:
        service = PersonService(db)
        result = await service.get_bed_number(query.page, query.page_size)
        return {
            "code": 200,
            "total": result["total"],
            "items": result["items"],
            "page": query.page,
            "page_size": query.page_size
        }
    except Exception as e:
        return {"code": 500, "message": str(e)}

@router.get("/", response_model=PersonListResponse)
async def get_persons(
    query: PersonQuery = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """获取人员简单信息列表"""
    try:
        service = PersonService(db)
        result = await service.get_persons_list(
            name=query.name,
            category=query.category,
            status=query.status,
            page=query.page,
            page_size=query.page_size
        )
        return {
            "code": 200,
            "total": result["total"],
            "items": result["items"],
            "page": query.page,
            "page_size": query.page_size
        }
    except Exception as e:
        return {"code": 500, "message": str(e)}

@router.get("/person/{pid}", response_model=PersonDetailResponse)
async def get_person(
    query: PersonID = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_role())
):
    """获取人员详细信息"""
    try:
        service = PersonService(db)
        person_detail = await service.get_person_detail(query.pid)
        return {"code": 200, "data": person_detail}
    except HTTPException as e:
        return {"code": e.status_code, "message": e.detail}
    except Exception as e:
        return {"code": 500, "message": str(e)}

@router.post("/", response_model=PersonCreateResponse)
async def create_person(
    person_data: PersonCreate,
    health_data: HealthBase,
    db: AsyncSession = Depends(get_db)
):
    """创建人员信息"""
    try:
        service = PersonService(db)
        result = await service.create_person(person_data, health_data)
        return {
            "code": 200,
            "message": "添加成功",
            "pid": result["person"].pid
        }
    except IntegrityError as e:
        await db.rollback()
        if "id_card" in str(e):
            return {"code": 400, "message": "身份证号已存在"}
        elif "phone" in str(e):
            return {"code": 400, "message": "手机号已存在"}
        return {"code": 500, "message": "数据库错误"}
    except Exception as e:
        await db.rollback()
        return {"code": 500, "message": str(e)}

@router.put("/{pid}", response_model=PersonCreateResponse)
async def update_person(
    pid: int,
    person_data: PersonCreate,
    health_data: HealthBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_role())
):
    """更新人员信息"""
    if current_user.role == "护理工":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="护理工无权访问此资源"
        )

    try:
        service = PersonService(db)
        await service.update_person(pid, person_data.dict(), health_data.dict())
        return {"code": 200, "message": "修改成功", "pid": pid}
    except IntegrityError as e:
        await db.rollback()
        if "id_card" in str(e):
            return {"code": 400, "message": "身份证号已存在"}
        elif "phone" in str(e):
            return {"code": 400, "message": "手机号已存在"}
        return {"code": 500, "message": "数据库错误"}
    except Exception as e:
        await db.rollback()
        return {"code": 500, "message": str(e)}

@router.delete("/{pid}")
async def delete_person(
    pid: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_role())
):
    """删除人员信息"""
    if current_user.role == "护理工":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="护理工无权访问此资源"
        )

    try:
        service = PersonService(db)
        await service.delete_person(pid)
        return {"code": 200, "message": "删除成功"}
    except Exception as e:
        await db.rollback()
        return {"code": 500, "message": str(e)}
