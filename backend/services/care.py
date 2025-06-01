# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.care import Care
from fastapi import HTTPException
from typing import List, Optional
from datetime import date, datetime

class CareService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_care_record(self, pid: int, caregiver_id: int, care_content: str,
                         care_date: date, evaluation: Optional[str] = None) -> Care:
        """创建护理记录"""
        record = Care(
            pid=pid,
            caregiver_id=caregiver_id,
            care_content=care_content,
            care_date=care_date,
            evaluation=evaluation,
            actual_time=datetime.now()
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_care_record_detail(self, care_id: int) -> Care:
        """获取护理记录详情"""
        stmt = select(Care).where(Care.care_id == care_id)
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="护理记录不存在")
        return record

    async def get_care_records_by_patient(self, pid: int, page: int = 1, page_size: int = 10) -> dict:
        """获取患者的护理记录(分页)"""
        # 获取总数
        count_stmt = select(Care).where(Care.pid == pid)
        count_result = await self.db.execute(count_stmt)
        total = len(count_result.scalars().all())

        # 获取分页数据
        stmt = select(Care)\
            .where(Care.pid == pid)\
            .order_by(Care.care_date.desc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return {
            "total": total,
            "items": items
        }

    async def get_care_records_by_caregiver(self, caregiver_id: int, page: int = 1, page_size: int = 10) -> dict:
        """获取护理员的护理记录(分页)"""
        # 获取总数
        count_stmt = select(Care).where(Care.caregiver_id == caregiver_id)
        count_result = await self.db.execute(count_stmt)
        total = len(count_result.scalars().all())

        # 获取分页数据
        stmt = select(Care)\
            .where(Care.caregiver_id == caregiver_id)\
            .order_by(Care.care_date.desc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return {
            "total": total,
            "items": items
        }

    async def update_care_record(self, record_id: int, care_content: Optional[str] = None,
                         care_date: Optional[date] = None, evaluation: Optional[str] = None) -> Care:
        """更新护理记录"""
        stmt = select(Care).where(Care.care_id == record_id)
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="护理记录不存在")

        if care_content:
            record.care_content = care_content
        if care_date:
            record.care_date = care_date
        if evaluation is not None:
            record.evaluation = evaluation
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete_care_record(self, record_id: int) -> None:
        """删除护理记录"""
        stmt = select(Care).where(Care.care_id == record_id)
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="护理记录不存在")

        await self.db.delete(record)
        await self.db.commit()
