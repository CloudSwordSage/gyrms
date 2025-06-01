# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 15:37:34
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : main.py
# @Desc    :

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.config import settings
from api import router as api_router

app = FastAPI()

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(.*\.)?cloudswordsage\.top(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router)

@app.get("/")
async def root():
    """
    test root
    """
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.development)
