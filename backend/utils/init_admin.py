import os
import asyncio
from utils.security import get_password_hash
from utils.database import get_db
from models.user import User
from sqlalchemy import select

async def init_admin():
    """初始化管理员账号"""
    async for session in get_db():
        # 检查是否已有管理员账号
        result = await session.execute(select(User).where(User.username == 'admin'))
        if result.scalar_one_or_none() is None:
            # 从.env读取管理员配置
            username = os.getenv('ADMIN_USERNAME', 'admin')
            password = get_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123'))
            role = os.getenv('ADMIN_ROLE', '管理员')
            real_name = os.getenv('ADMIN_REAL_NAME', '系统管理员')
            phone = os.getenv('ADMIN_PHONE', '13800000000')

            # 创建管理员账号
            admin = User(
                username=username,
                password=password,
                real_name=real_name,
                role=role,
                phone=phone,
                is_activate=True
            )
            session.add(admin)
            await session.commit()
            print("管理员账号创建成功")
            print(f"用户名: {username}")
            print(f"密码: {password}")
        else:
            print("管理员账号已存在")

if __name__ == "__main__":
    asyncio.run(init_admin())
