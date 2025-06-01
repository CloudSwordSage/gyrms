# -*- coding: utf-8 -*-
# @Time    : 2025/4/29 16:29:14
# @Author  : 墨烟行(GitHub UserName: CloudSwordSage)
# @File    : create_user.py
# @Desc    :


from config.config import settings

# 创建数据库及用户，权限分配
import pymysql

conn = pymysql.connect(
    host=settings.mysql_host,
    port=settings.mysql_port,
    user='root',
    password='aserttdsdcgrfswfszf',
    charset='utf8mb4'
)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.mysql_db}")
cursor.execute(f"CREATE USER IF NOT EXISTS '{settings.mysql_user}'@'%' IDENTIFIED BY '{settings.mysql_password}'")
cursor.execute(f"GRANT ALL PRIVILEGES ON {settings.mysql_db}.* TO '{settings.mysql_user}'@'%'")
cursor.execute(f"FLUSH PRIVILEGES")
cursor.close()
conn.commit()
conn.close()
