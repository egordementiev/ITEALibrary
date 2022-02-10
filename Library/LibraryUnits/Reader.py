"""
Модуль для описания сущности "Читатель"
"""
from typing import Union
from Library.DataBase.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean, Text, ForeignKey


class Reader(Base):
    __tablename__ = 'readers'

    ID = Column(Integer, primary_key=True)
    name = Column(Text)
    surname = Column(Text)
    patronymic = Column(Text)
    age = Column(Integer)
    is_admin = Column(Boolean)

    email = Column(Text, unique=True)
    password = Column(Text, unique=True)

    def __init__(self,
                 ID: Union[int, None],
                 name: str,
                 surname: str,
                 patronymic: str,
                 age: int,
                 is_admin: bool,
                 email: str,
                 password: str):

        self.ID = ID
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.age = age
        self.is_admin = is_admin
        self.email = email
        self.password = password

    def __repr__(self):
        return f'({self.ID}) {self.surname} {self.name} {self.patronymic} | {self.age}'
