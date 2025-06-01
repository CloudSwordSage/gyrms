alembic revision --autogenerate -m "create account table"
alembic upgrade head
python -m utils.init_admin
