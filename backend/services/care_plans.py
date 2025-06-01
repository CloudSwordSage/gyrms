# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.care_plan import CarePlan
from schema.care_plan import CarePlanCreate
from models.user import User
from fastapi import HTTPException
from typing import List

class CarePlanService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_plan_by_id(self, plan_id: int) -> CarePlan:
        """根据ID获取护理计划"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_care_plan(self, plan_data: CarePlanCreate) -> CarePlan:
        """创建新的护理计划"""
        # 验证person是否存在
        from models.person import Person
        stmt = select(Person).where(Person.pid == plan_data.pid)
        result = await self.db.execute(stmt)
        if not result.scalars().first():
            raise HTTPException(
                status_code=400,
                detail=f"人员ID {plan_data.pid} 不存在"
            )

        db_plan = CarePlan(
            pid=plan_data.pid,
            plan_name=plan_data.plan_name,
            plan_content=plan_data.plan_content,
            frequency=plan_data.frequency,
            start_date=plan_data.start_date,
            end_date=plan_data.end_date,
            status='进行中'
        )
        self.db.add(db_plan)
        await self.db.commit()
        await self.db.refresh(db_plan)
        return db_plan

    async def accept_plan(self, plan_id: int, user_id: int) -> CarePlan:
        """接取护理任务"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        plan = result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="任务不存在")
        if plan.executor_id:
            raise HTTPException(status_code=400, detail="任务已被接取")

        plan.executor_id = user_id
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def abandon_plan(self, plan_id: int, user_id: int) -> CarePlan:
        """放弃护理任务"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        plan = result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="任务不存在")
        if plan.executor_id != user_id:
            raise HTTPException(status_code=403, detail="无权放弃此任务")

        plan.executor_id = None
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def transfer_plan(self, plan_id: int, from_user_id: int, to_user_id: int) -> CarePlan:
        """转交护理任务"""
        # 查询护理计划
        plan_stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        plan_result = await self.db.execute(plan_stmt)
        plan = plan_result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="任务不存在")
        if plan.executor_id != from_user_id:
            raise HTTPException(status_code=403, detail="无权转交此任务")

        # 验证新执行者是否存在
        user_stmt = select(User).where(User.uid == to_user_id)
        user_result = await self.db.execute(user_stmt)
        new_executor = user_result.scalars().first()
        if not new_executor:
            raise HTTPException(status_code=404, detail="新执行者不存在")

        plan.executor_id = to_user_id
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def assign_task(self, plan_id: int, executor_id: int, assign_type: str) -> CarePlan:
        """分配护理任务"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        plan = result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="任务不存在")

        plan.executor_id = executor_id
        plan.status = '进行中'
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def get_available_plans(self, page: int = 1, page_size: int = 10) -> List[CarePlan]:
        """获取可接取的任务列表"""
        stmt = select(CarePlan)\
            .where(CarePlan.executor_id == None)\
            .where(CarePlan.status == '进行中')\
            .order_by(CarePlan.start_date.asc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        # total
        total_stmt = select(func.count())\
            .where(CarePlan.executor_id == None)\
            .where(CarePlan.status == '进行中')\
            .order_by(CarePlan.start_date.asc())
        total = await self.db.execute(total_stmt)
        result = await self.db.execute(stmt)
        return {
            "total": total.scalars().first(),
            "items": result.scalars().all()
        }

    async def get_my_plans(self, executor_id: int, page: int = 1, page_size: int = 10) -> List[CarePlan]:
        """获取执行者自己的任务列表"""
        stmt = select(CarePlan)\
            .where(CarePlan.executor_id == executor_id)\
            .order_by(CarePlan.start_date.asc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        result = await self.db.execute(stmt)
        total_stmt = select(func.count())\
            .where(CarePlan.executor_id == executor_id)
        total = await self.db.execute(total_stmt)
        return {
            "total": total.scalars().first(),
            "items": result.scalars().all()
        }

    async def get_all_plans(self, page: int = 1, page_size: int = 10) -> List[CarePlan]:
        """获取所有任务列表(管理员使用)"""
        stmt = select(CarePlan)\
            .order_by(CarePlan.start_date.asc())\
            .limit(page_size)\
            .offset((page - 1) * page_size)
        result = await self.db.execute(stmt)
        total_stmt = select(func.count())
        total = await self.db.execute(total_stmt)
        return {
            "total": total.scalars().first(),
            "items": result.scalars().all()
        }

    async def complete_plan(self, plan_id: int, executor_id: int) -> CarePlan:
        """完成任务"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        plan = result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="任务不存在")
        if plan.executor_id != executor_id:
            raise HTTPException(status_code=403, detail="无权完成此任务")

        plan.status = '已结束'
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def get_person_plans(self, pid: int) -> List[CarePlan]:
        """获取指定人员的所有护理计划"""
        stmt = select(CarePlan)\
            .where(CarePlan.pid == pid)\
            .order_by(CarePlan.start_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_plan(self, plan_id: int) -> None:
        """删除护理计划"""
        stmt = select(CarePlan).where(CarePlan.plan_id == plan_id)
        result = await self.db.execute(stmt)
        plan = result.scalars().first()
        if not plan:
            raise HTTPException(status_code=404, detail="护理计划不存在")

        await self.db.delete(plan)
        await self.db.commit()
