from Library.DataBase.DataBase import DataBaseJSON
from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from Library.LibraryUnits.Admin import Admin


class BookDataBase:
    """Класс описывающий работу с базой данных для класса Book"""
    def __init__(self, data_base_path):
        self.__db = DataBaseJSON()
        self.__data_base_path = data_base_path

    def write_to_db(self, books: list, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path
        write_data = {'books': [self.__encode(book) for book in books]}
        self.__db.write_to_db(write_data, data_base_path)

    def read_from_db(self, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path
        try:
            return [self.__decode(data) for data in self.__db.read_from_db(data_base_path)['books']]
        except:
            return None

    @staticmethod
    def __encode(book):
        field_dict = {}
        for field in book.__dict__:
            if callable(field):
                continue
            field_dict[field.replace(f'_{book.__class__.__name__}__', '')] = book.__getattribute__(field)
        return field_dict

    @staticmethod
    def __decode(book_dict):
        return Book(book_dict['title'], book_dict['author'], book_dict['year'], book_dict['id'], book_dict['reader_id'])


class ReaderDataBase:
    """Класс описывающий работу с базой данных для класса Reader"""
    def __init__(self, data_base_path):
        self.__db = DataBaseJSON()
        self.__data_base_path = data_base_path

    def write_to_db(self, readers: list, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path

        write_data = {'readers': [self.__encode(reader) for reader in readers]}
        self.__db.write_to_db(write_data, data_base_path)

    def read_from_db(self, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path
        try:
            return [self.__decode(data) for data in self.__db.read_from_db(data_base_path)['readers']]
        except:
            return []

    @staticmethod
    def __encode(reader):
        field_dict = {}
        for field in reader.__dict__:
            if callable(field):
                continue
            field_dict[field.replace(f'_{reader.__class__.__name__}__', '')] = reader.__getattribute__(field)
        return field_dict

    @staticmethod
    def __decode(reader_dict):
        return Reader(reader_dict['name'], reader_dict['surname'], reader_dict['patronymic'],
                      reader_dict['age'], reader_dict['id'])


class AdminDataBase:
    """Класс описывающий работу с базой данных для класса Admin"""

    def __init__(self, data_base_path):
        self.__db = DataBaseJSON()
        self.__data_base_path = data_base_path

    def write_to_db(self, readers: list, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path

        write_data = {'admins': [self.__encode(reader) for reader in readers]}
        self.__db.write_to_db(write_data, data_base_path)

    def read_from_db(self, data_base_path=None):
        if not data_base_path:
            data_base_path = self.__data_base_path
        try:
            return [self.__decode(data) for data in self.__db.read_from_db(data_base_path)['admins']]
        except:
            return []

    @staticmethod
    def __encode(admin):
        field_dict = {}
        for field in admin.__dict__:
            if callable(field):
                continue
            field_dict[field.replace(f'_{admin.__class__.__name__}__', '')] = admin.__getattribute__(field)
        return field_dict

    @staticmethod
    def __decode(reader_dict):
        return Admin(reader_dict['name'], reader_dict['surname'], reader_dict['user_id'], reader_dict['add_by'])