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

    def __init__(self,
                 ID: Union[int, None],
                 name: str,
                 surname: str,
                 patronymic: str,
                 age: int):

        self.ID = ID
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.age = age

    def __repr__(self):
        return f'({self.ID}) {self.surname} {self.name} {self.patronymic} | {self.age}'
