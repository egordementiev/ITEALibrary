from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from Library.DataBase.DataBase import DataBasePostgreSQL
from typing import Union


class Library:
    def __init__(self):
        self.__data_base = DataBasePostgreSQL()

    def add_book(self, title: str, author: str, year: int):
        """Добавление книги"""
        self.__data_base.add_book(Book(title, author, year))
        print('Done: book was successfully added to the library')
        return 'Done'

    def add_reader(self, name: str, surname: str, patronymic: str, year: int):
        """Добавление читателя"""
        self.__data_base.add_reader(Reader(name, surname, patronymic, year))
        print(f'Done: reader was successfully added to the library')
        return 'Done'

    def del_book(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            if not book.get_reader_id():
                self.__data_base.delete_book(book)
                return 'Done'
            return 'Error, this book has reader'
        return 'Error, this book is not in the library'

    def del_reader(self, reader_id):
        reader = self.get_reader_by_id(reader_id)
        if reader:
            for book in self.__data_base.get_books():
                if book.get_reader_id() == reader_id:
                    return 'Error, this reader has a book'
            self.__data_base.delete_reader(reader)
            return 'Done'
        return 'Error, this reader is not in the library'

    def give_book(self, book_id: int, reader_id: int):
        """
        Фукция выдачи книги читателю

        :param book_id: id книги, которую возвращаем
        :param reader_id: id читателя, который возвращает книгу
        """
        book = self.get_book_by_id(book_id)
        if not book:
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.get_reader_by_id(reader_id)
        if not reader:
            print(f'Error: reader with id {reader_id} is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.get_reader_id() is not None:
            print(f'Error: book with id {book_id} are out of stock')
            return 'Error: book with this id are out of stock'

        book.set_reader_id(reader_id)
        self.__data_base.update_book(book)

    def return_book(self, book_id: int, reader_id: int):
        """
        Функция возврата книги библиотеку

        :param book_id: id книги, которую возвращаем
        :param reader_id: id читателя, который возвращает книгу
        """
        book = self.get_book_by_id(book_id)
        if not book:
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.get_reader_by_id(reader_id)
        if not reader:
            print(f'Error: reader with this id is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.get_reader_id() != reader.get_id():
            print(f'Error: book with this id is not '
                  f'in the possession of the reader'
                  f'{reader.get_name()} {reader.get_surname()}')
            return 'Error: book with this id is not in the possession of the reader'

        book.set_reader_id(None)
        self.__data_base.update_book(book)

    def get_books(self, sort: str = 'id', reverse: bool = False):
        if sort not in ['id', 'title', 'author', 'year']:
            sort = 'id'

        def get_sort_field_book(obj: Book):
            if sort == 'id':
                return int(obj.get_id())
            elif sort == 'title':
                return obj.get_title()
            elif sort == 'author':
                return obj.get_author()
            elif sort == 'year':
                return int(obj.get_year())

        books = [book for book in sorted(self.__data_base.get_books(), key=get_sort_field_book, reverse=reverse)]
        return books, sort

    def get_readers(self, sort):
        if sort not in ['id', 'name', 'surname', 'year']:
            print(sort)
            sort = 'id'

        def get_sort_field_reader(obj: Reader):
            if sort == 'id':
                return int(obj.get_id())
            elif sort == 'name':
                return obj.get_name()
            elif sort == 'surname':
                return obj.get_surname()
            elif sort == 'year':
                return int(obj.get_age())

        readers = [reader for reader in sorted(self.__data_base.get_readers(), key=get_sort_field_reader)]
        return [readers, sort]

    def get_book_by_id(self, book_id: int) -> Union[Book, None]:
        """
        Функция получения книги по id из списка книг

        :param book_id: id книги, которую хотим получить
        :return: obj Book (если книга есть в библиотеке); None (если книги нет)
        """
        for book in self.__data_base.get_books():
            print(f'{book.get_id()} ({type(book.get_id())}) == {book_id} '
                  f'({type(book_id)}) - {book.get_id() == book_id}')
            if book.get_id() == book_id:
                return book
        return None

    def get_reader_by_id(self, reader_id: int) -> Union[Reader, None]:
        """
        Функция получения читателя по id из списка читателей

        :param reader_id: id читателя
        :return: obj Reader (если читатель есть в библиотеке); None (если читателя нет)
        """
        for reader in self.__data_base.get_readers():
            if reader.get_id() == reader_id:
                return reader
        return None
