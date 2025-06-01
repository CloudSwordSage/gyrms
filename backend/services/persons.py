# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.person import Person
from models.health import Health
from schema.person import PersonCreate, HealthCreate
from fastapi import HTTPException
from typing import Dict, List, Optional

class HealthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_health(self, pid: int, health_data: dict) -> Health:
        """创建健康记录"""
        health = Health(pid=pid, **health_data)
        self.db.add(health)
        await self.db.flush()
        await self.db.refresh(health)
        return health

    async def get_health_records(self, pid: int) -> Health:
        """获取患者的健康记录"""
        from sqlalchemy import select
        stmt = select(Health)\
            .where(Health.pid == pid)\
            .order_by(Health.last_checkup_date.desc())
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            record = Health(pid=pid)
        return record

    async def update_health_record(self, record_id: int, update_data: dict) -> Health:
        """更新健康记录"""
        from sqlalchemy import select
        stmt = select(Health).where(Health.health_id == record_id)
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="健康记录不存在")

        for key, value in update_data.items():
            setattr(record, key, value)

        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete_health_record(self, record_id: int) -> None:
        """删除健康记录"""
        from sqlalchemy import select
        stmt = select(Health).where(Health.health_id == record_id)
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="健康记录不存在")

        await self.db.delete(record)
        await self.db.commit()


class PersonService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_persons_list(self, name: Optional[str] = None,
                            category: Optional[str] = None,
                            status: str = 'in',
                            page: int = 1,
                            page_size: int = 20) -> Dict:
        """获取人员简单信息列表(带名称模糊查询)"""
        stmt = select(
            Person.pid,
            Person.name,
            Person.gender,
            Person.age,
            Person.category,
            Person.bed_number,
            Person.check_in_date,
            Person.check_out_date,
            Person.photo
        )

        if name:
            stmt = stmt.where(Person.name.ilike(f"%{name}%"))
        if category:
            stmt = stmt.where(Person.category == category)
        if status == 'in':
            stmt = stmt.where(Person.check_out_date == None)
        elif status == 'out':
            stmt = stmt.where(Person.check_out_date != None)

        # 获取总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.execute(count_stmt)

        # 获取分页数据
        results = await self.db.execute(
            stmt.offset((page-1)*page_size).limit(page_size))

        return {
            "total": total.scalar_one(),
            "items": [row._asdict() for row in results.all()]
        }

    async def get_bed_number(self, page=1, page_size=10) -> Dict:
        """获取所有床位号"""
        stmt = select(Person.pid, Person.bed_number)
        # 获取总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.execute(count_stmt)

        # 获取分页数据
        results = await self.db.execute(
            stmt.offset((page-1)*page_size).limit(page_size))

        return {
            "total": total.scalar_one(),
            "items": [row._asdict() for row in results.all()]
        }

    async def get_person_detail(self, pid: int) -> Dict:
        """获取人员详细信息(包含健康信息)"""
        person_stmt = select(Person).where(Person.pid == pid)
        person_result = await self.db.execute(person_stmt)
        person = person_result.scalars().first()
        if not person:
            raise HTTPException(status_code=404, detail="人员不存在")

        health_service = HealthService(self.db)
        health = await health_service.get_health_records(pid)

        # 构建干净的person_data字典
        person_data = {
            "pid": person.pid,
            "name": person.name,
            "gender": person.gender,
            "age": person.age,
            "id_card": person.id_card,
            "phone": person.phone,
            "emergency_contact": person.emergency_contact,
            "emergency_phone": person.emergency_phone,
            "category": person.category,
            "bed_number": person.bed_number,
            "check_in_date": person.check_in_date,
            "check_out_date": person.check_out_date,
            "check_out_reason": person.check_out_reason,
            "photo": person.photo
        }

        # 构建干净的health_data字典
        health_data = None
        if health:
            health_data = {
                "health_id": health.health_id,
                "pid": health.pid,
                "disease_history": health.disease_history,
                "allergy_history": health.allergy_history,
                "blood_pressure": health.blood_pressure,
                "blood_glucose": health.blood_glucose,
                "last_checkup_date": health.last_checkup_date,
                "medical_history": health.medical_history
            }

        return {
            "person_data": person_data,
            "health_data": health_data
        }

    async def create_person(self, person_data: PersonCreate, health_data: HealthCreate) -> Dict:
        """创建人员信息(同时创建健康记录)"""
        async with self.db.begin():
            # 创建人员记录
            person = Person(**person_data.model_dump())
            self.db.add(person)
            await self.db.flush()

            # 创建健康记录
            if health_data:
                health_service = HealthService(self.db)
                health = await health_service.create_health(pid=person.pid, health_data=health_data.model_dump())

            await self.db.refresh(person)
            return {"person": person}

    async def update_person(self, pid: int, person_data: Dict, health_data: Dict) -> Dict:
        """更新人员信息(同时更新健康记录)"""
        # 获取人员记录
        person_stmt = select(Person).where(Person.pid == pid)
        person_result = await self.db.execute(person_stmt)
        person = person_result.scalars().first()
        if not person:
            raise HTTPException(status_code=404, detail="人员不存在")

        # 更新人员信息
        for key, value in person_data.items():
            if hasattr(person, key):
                setattr(person, key, value)

        # 更新健康记录
        health_service = HealthService(self.db)
        health = await health_service.get_health_records(pid)
        if health and health_data:
            await health_service.update_health_record(health.health_id, health_data)

        await self.db.commit()
        await self.db.refresh(person)
        return {"person": person}


    async def delete_person(self, pid: int) -> None:
        """删除人员信息及关联记录(健康记录、护理计划)"""
        from services.care_plans import CarePlanService

        # 查询人员记录
        stmt = select(Person).where(Person.pid == pid)
        result = await self.db.execute(stmt)
        person = result.scalars().first()
        if not person:
            raise HTTPException(status_code=404, detail="人员不存在")

        # 删除健康记录
        health_service = HealthService(self.db)
        health = await health_service.get_health_records(pid)
        if health and health.health_id:
            await health_service.delete_health_record(health.health_id)

        # 删除关联的护理计划
        care_plan_service = CarePlanService(self.db)
        care_plans = await care_plan_service.get_person_plans(pid)
        for plan in care_plans:
            await care_plan_service.delete_plan(plan.plan_id)

        # 最后删除人员信息
        await self.db.delete(person)
        await self.db.commit()
