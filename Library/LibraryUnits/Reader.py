"""
Модуль для описания сущности "Читатель"
"""


class Reader:
    def __init__(self,
                 name: str,
                 surname: str,
                 patronymic: str,
                 age: int,
                 _id: int = None):

        self.__id = _id
        self.__name = name
        self.__surname = surname
        self.__patronymic = patronymic
        self.__age = age

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_patronymic(self):
        return self.__patronymic

    def get_age(self):
        return self.__age

    def set_name(self, name):
        self.__name = name

    def set_surname(self, surname):
        self.__surname = surname

    def set_patronymic(self, patronymic):
        self.__patronymic = patronymic

    def set_age(self, age):
        self.__age = age

    def __repr__(self):
        return f'({self.__id}) {self.__surname} {self.__name} {self.__patronymic} | {self.__age}'
