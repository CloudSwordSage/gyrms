from sqlalchemy import Column, Integer, String, Date, Enum, Text

from .base import Base

class Person(Base):
    __tablename__ = "person"

    pid = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum('男', '女', name='gender_enum'), nullable=False)
    age = Column(Integer, nullable=False)
    id_card = Column(String(18), unique=True, nullable=False)
    phone = Column(String(11), nullable=False)
    emergency_contact = Column(String(50), nullable=False)
    emergency_phone = Column(String(11), nullable=False)
    category = Column(Enum('孤寡老人', '残障人士', '短期托管', name='category_enum'), nullable=False)
    bed_number = Column(String(20), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date)
    check_out_reason = Column(String(100))
    photo = Column(Text)
