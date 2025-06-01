# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .persons import router as persons_router
from .reminders import router as reminders_router
from .care import router as care_router
from .care_plans import router as care_plans_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(persons_router)
router.include_router(reminders_router)
router.include_router(care_router)
router.include_router(care_plans_router)
