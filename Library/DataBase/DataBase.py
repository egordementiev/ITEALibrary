from abc import ABC, abstractmethod



class DataBase(ABC):
    @abstractmethod
    def __init__(self, port, ip):
        pass

    @abstractmethod
    def add_book(self, book):
        pass

    @abstractmethod
    def update_book(self, book):
        pass

    @abstractmethod
    def delete_book(self, book):
        pass

    @abstractmethod
    def add_reader(self, reader):
        pass

    @abstractmethod
    def update_reader(self, reader):
        pass

    @abstractmethod
    def delete_reader(self, reader):
        pass


# class DataBaseJSON(DataBase):
#     def write_to_db(self, write_data, data_base_title):
#         with open(data_base_title, 'w') as file:
#             json.dump(write_data, file, indent=2)
#
#     def read_from_db(self, data_base_title):
#         with open(data_base_title, 'r') as file:
#             data = json.load(file)
#             return data


class DataBasePostgreSQL(DataBase):
    """ Клас описывающий роботу с базой данных PostgreSQL """
    def __init__(self, port='5433', ip='localhost', password='fagSxElh3f2c5_', dbname='postgres', user='postgres'):


    def add_book(self, book):
        """Добавление книги"""
        pass

    def update_book(self, book):
        pass

    def delete_book(self, book):
        pass

    def add_reader(self, reader):
        pass

    def update_reader(self, reader):
        pass

    def delete_reader(self, reader):
        pass


