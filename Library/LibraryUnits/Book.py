"""
Модуль для описания сущности "Книга"
"""
from typing import Union
from Library.DataBase.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean, Text, ForeignKey


class Book(Base):
    __tablename__ = 'books'

    ID = Column(Integer, primary_key=True)
    title = Column(Text)
    author = Column(Text)
    year = Column(Integer)
    reader_id = Column(Integer, ForeignKey('readers.ID'))

    def __init__(self,
                 _id: Union[int, None],
                 title: str,
                 author: str,
                 year: int,
                 reader_id: int = None):
        self.ID = _id
        self.title = title
        self.author = author
        self.year = year
        self.reader_id = reader_id

    def __repr__(self):
        return f'{self.ID} | "{self.title}" | {self.author} | {self.year} | reader = {self.reader_id}'
