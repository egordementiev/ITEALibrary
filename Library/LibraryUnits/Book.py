"""
Модуль для описания сущности "Книга"
"""
from typing import Union


class Book:
    def __init__(self,
                 title: str,
                 author: str,
                 year: int,
                 _id: int = None,
                 reader_id: int = None):

        self.__id = _id if _id is not None else int(id(self))
        self.__title = title
        self.__author = author
        self.__year = year
        self.__reader_id = reader_id

    def get_id(self) -> int:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_author(self) -> str:
        return self.__author

    def get_year(self) -> int:
        return self.__year

    def get_reader_id(self) -> Union[int, None]:
        return self.__reader_id

    def set_title(self, title: str):
        self.__title = title

    def set_author(self, author: str):
        self.__author = author

    def set_year(self, year: int):
        self.__year = year

    def set_reader_id(self, reader_id: Union[int, None]):
        self.__reader_id = reader_id

    def __repr__(self):
        return f'{self.__id} | "{self.__title}" | {self.__author} | {self.__year} | reader = {self.__reader_id}'
