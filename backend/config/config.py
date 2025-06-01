# -*- coding: utf-8 -*-
# @Time    : 2025/4/25 15:42:33
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : config.py
# @Desc    :

import os
import base64
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def decode_key(base64_key: str) -> str:
    """Base64解码密钥并验证格式"""
    if not base64_key:
        raise ValueError("Empty key provided")

    try:
        decoded = base64.b64decode(base64_key).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decode key: {str(e)}")

    # 简单的PEM格式验证
    if "-----BEGIN" not in decoded or "-----END" not in decoded:
        raise ValueError("Decoded key is not in PEM format")

    return decoded
@dataclass
class Settings:
    mysql_host: str = os.getenv("MYSQL_HOST")
    mysql_port: int = int(os.getenv("MYSQL_PORT"))
    mysql_user: str = os.getenv("MYSQL_USER")
    mysql_password: str = os.getenv("MYSQL_PASSWORD")
    mysql_db: str = os.getenv("MYSQL_DATABASE")
    mysql_url: str = f"mysql+asyncmy://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = int(os.getenv("REDIS_PORT"))
    redis_db: int = int(os.getenv("REDIS_DB"))
    redis_decode_responses: bool = os.getenv("REDIS_DECODE_RESPONSES") == "True"
    @property
    def private_key(self):
        base64_key = os.getenv("PRIVATE_KEY")
        if not base64_key:
            raise ValueError("PRIVATE_KEY environment variable is not set")
        return decode_key(base64_key)
    @property
    def public_key(self):
        base64_key = os.getenv("PUBLIC_KEY")
        if not base64_key:
            raise ValueError("PUBLIC_KEY environment variable is not set")
        return decode_key(base64_key)
    development: bool = os.getenv("DEVELOPMENT") == "True"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080").split()[0])  # 默认7天(60*24*7)
settings = Settings()

