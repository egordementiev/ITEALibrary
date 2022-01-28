import psycopg2
from psycopg2.extras import NamedTupleCursor
from abc import ABC, abstractmethod
from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader


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
    def __init__(self, port='5432', host='localhost', password='fagSxElh3f2c5_', dbname='postgres', user='postgres'):
        self.conn = psycopg2.connect(dbname=dbname,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)
        self.conn.autocommit = True
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS "readers" ('
                           '"ID" SMALLSERIAL, '
                           '"name" TEXT, '
                           '"surname" TEXT, '
                           '"patronymic" TEXT, '
                           '"age" INTEGER, '
                           'PRIMARY KEY ("ID"))')
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS "books" ('
                           '"ID" SMALLSERIAL, '
                           '"title" TEXT, '
                           '"author" TEXT, '
                           '"year" INTEGER, '
                           '"reader_id" INTEGER, '
                           'PRIMARY KEY ("ID"), '
                           'FOREIGN KEY ("reader_id") REFERENCES "readers"("ID"))')

    def add_book(self, book: Book):
        """Добавление книги"""
        title = book.get_title()
        author = book.get_author()
        year = book.get_year()
        reader_id = book.get_reader_id()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO "books" ("title", "author", "year", "reader_id") VALUES (%s, %s, %s, %s)',
                (title, author, year, reader_id))

    def update_book(self, book: Book):
        ID = book.get_id()
        title = book.get_title()
        author = book.get_author()
        year = book.get_year()
        reader_id = book.get_reader_id()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'UPDATE "books" SET "title" = %s, "author" = %s, "year" = %s, "reader_id" = %s WHERE "ID" = %s',
                (title, author, year, reader_id, ID))

    def delete_book(self, book: Book):
        ID = book.get_id()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('DELETE FROM "books" WHERE "ID" = %s', (ID,))

    def add_reader(self, reader: Reader):
        name = reader.get_name()
        surname = reader.get_surname()
        patronymic = reader.get_patronymic()
        age = reader.get_age()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO "readers" ("name", "surname", "patronymic", "age") VALUES (%s, %s, %s, %s)',
                (name, surname, patronymic, age))

    def update_reader(self, reader: Reader):
        ID = reader.get_id()
        name = reader.get_name()
        surname = reader.get_surname()
        patronymic = reader.get_patronymic()
        age = reader.get_age()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'UPDATE "readers" SET "name" = %s, "surname" = %s, "patronymic" = %s, "age" = %s WHERE "ID" = %s',
                (name, surname, patronymic, age, ID))

    def delete_reader(self, reader: Reader):
        ID = reader.get_id()
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('DELETE FROM "readers" WHERE "ID" = %s', (ID,))

    def get_books(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM "books"')
            books = [Book(book.title, book.author, book.year, book.ID, book.reader_id) for book in cursor.fetchall()]
            print(books)
            return books

    def get_readers(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM "readers"')
            readers = [Reader(reader.name, reader.surname, reader.patronymic, reader.age, reader.ID)
                       for reader in cursor.fetchall()]
            return readers


