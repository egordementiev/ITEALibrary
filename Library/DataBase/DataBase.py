from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Library.DataBase.DataBaseConfig import Base
from abc import ABC, abstractmethod
from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from typing import Union


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

    @abstractmethod
    def get_book(self, ID):
        pass

    @abstractmethod
    def get_reader(self, ID):
        pass

    @abstractmethod
    def get_reader_by_email(self, email):
        pass

    @abstractmethod
    def get_books(self):
        pass

    @abstractmethod
    def get_readers(self):
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


# class DataBasePostgreSQL(DataBase):
#     """ Клас описывающий роботу с базой данных PostgreSQL """
#     def __init__(self, port='5432', host='localhost', password='123', dbname='postgres', user='postgres'):
#         self.conn = psycopg2.connect(dbname=dbname,
#                                      user=user,
#                                      password=password,
#                                      host=host,
#                                      port=port)
#         self.conn.autocommit = True
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('CREATE TABLE IF NOT EXISTS "readers" ('
#                            '"ID" SMALLSERIAL, '
#                            '"name" TEXT, '
#                            '"surname" TEXT, '
#                            '"patronymic" TEXT, '
#                            '"age" INTEGER, '
#                            'PRIMARY KEY ("ID"))')
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('CREATE TABLE IF NOT EXISTS "books" ('
#                            '"ID" SMALLSERIAL, '
#                            '"title" TEXT, '
#                            '"author" TEXT, '
#                            '"year" INTEGER, '
#                            '"reader_id" INTEGER, '
#                            'PRIMARY KEY ("ID"), '
#                            'FOREIGN KEY ("reader_id") REFERENCES "readers"("ID"))')
#
#     def add_book(self, book: Book):
#         """Добавление книги"""
#         title = book.get_title()
#         author = book.get_author()
#         year = book.get_year()
#         reader_id = book.get_reader_id()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute(
#                 'INSERT INTO "books" ("title", "author", "year", "reader_id") VALUES (%s, %s, %s, %s)',
#                 (title, author, year, reader_id))
#
#     def update_book(self, book: Book):
#         ID = book.get_id()
#         title = book.get_title()
#         author = book.get_author()
#         year = book.get_year()
#         reader_id = book.get_reader_id()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute(
#                 'UPDATE "books" SET "title" = %s, "author" = %s, "year" = %s, "reader_id" = %s WHERE "ID" = %s',
#                 (title, author, year, reader_id, ID))
#
#     def delete_book(self, book: Book):
#         ID = book.get_id()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('DELETE FROM "books" WHERE "ID" = %s', (ID,))
#
#     def add_reader(self, reader: Reader):
#         name = reader.get_name()
#         surname = reader.get_surname()
#         patronymic = reader.get_patronymic()
#         age = reader.get_age()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute(
#                 'INSERT INTO "readers" ("name", "surname", "patronymic", "age") VALUES (%s, %s, %s, %s)',
#                 (name, surname, patronymic, age))
#
#     def update_reader(self, reader: Reader):
#         ID = reader.get_id()
#         name = reader.get_name()
#         surname = reader.get_surname()
#         patronymic = reader.get_patronymic()
#         age = reader.get_age()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute(
#                 'UPDATE "readers" SET "name" = %s, "surname" = %s, "patronymic" = %s, "age" = %s WHERE "ID" = %s',
#                 (name, surname, patronymic, age, ID))
#
#     def delete_reader(self, reader: Reader):
#         ID = reader.get_id()
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('DELETE FROM "readers" WHERE "ID" = %s', (ID,))
#
#     def get_books(self):
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('SELECT * FROM "books"')
#             books = [Book(book.title, book.author, book.year, book.ID, book.reader_id) for book in cursor.fetchall()]
#             print(books)
#             return books
#
#     def get_readers(self):
#         with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute('SELECT * FROM "readers"')
#             readers = [Reader(reader.name, reader.surname, reader.patronymic, reader.age, reader.ID)
#                        for reader in cursor.fetchall()]
#             return readers


class DataBaseSQLAlchemy(DataBase):
    """ Клас описывающий роботу с базой данных PostgreSQL """
    def __init__(self, dbport='5434', dbhost='localhost', dbpassword='123', dbname='postgres', dbuser='postgres'):
        self.engine = create_engine(f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}')
        Base.metadata.create_all(self.engine)

    def add_book(self, book: Book):
        """Добавление книги"""
        session = Session(self.engine)
        try:
            session.add(book)  # Добавляем книгу в базу данных
            session.commit()
        except:
            return False
        finally:
            session.close()

    def update_book(self, book: Book):
        session = Session(self.engine)
        old_book = session.query(Book).filter_by(ID=book.ID).first()  # Берем книгу из бд
        print(old_book)
        old_book.title = book.title  # Обновляем поле title
        old_book.author = book.author  # Обновляем поле author
        old_book.year = book.year  # Обновляем поле year
        old_book.reader_id = book.reader_id  # Обновляем поле reader_id
        print(session.dirty)
        session.commit()

    def delete_book(self, book: Book):
        session = Session(self.engine)
        session.delete(book)  # Удаляем книгу из базы данных
        session.commit()
        session.close()

    def add_reader(self, reader: Reader):
        session = Session(self.engine)
        try:
            session.add(reader)  # Добавляем читателя в базу данных
            session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            session.close()

    def update_reader(self, reader: Reader):
        session = Session(self.engine)
        old_reader = session.query(Reader).filter_by(ID=reader.ID).first()  # Берем книгу из бд
        print(old_reader)
        old_reader.name = reader.name  # Обновляем поле name
        old_reader.surname = reader.surname  # Обновляем поле surname
        old_reader.patronymic = reader.patronymic  # Обновляем поле patronymic
        old_reader.age = reader.age  # Обновляем поле age
        old_reader.is_admin = reader.is_admin  # Обновляем поле is_admin
        print(session.dirty)
        session.commit()

    def delete_reader(self, reader: Reader):
        session = Session(self.engine)
        session.delete(reader)  # Удаляю читателя из базы данных
        session.commit()
        session.close()

    def get_book(self, ID) -> Union[Book, None]:
        session = Session(self.engine)
        try:
            book = session.query(Book).filter_by(ID=ID).first()  # Берем книгу из бд
        except:
            return None
        session.close()
        return book

    def get_reader(self, ID):
        session = Session(self.engine)
        try:
            reader = session.query(Reader).filter_by(ID=ID).first()  # Берем читателя из бд
        except:
            return None
        session.close()
        return reader

    def get_reader_by_email(self, email):
        session = Session(self.engine)
        try:
            reader = session.query(Reader).filter_by(email=email).first()  # Берем читателя из бд по email
        except:
            return None
        session.close()
        return reader

    def get_books(self):
        session = Session(self.engine)
        books = session.query(Book).all()  # Берем все книги из бд
        session.close()
        return books

    def get_readers(self):
        session = Session(self.engine)
        readers = session.query(Reader).all()  # Берем всех читателей из бд
        session.close()
        return readers

