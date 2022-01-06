from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from Library.LibraryUnits.WorkWithDataBase.LibraryUnitsDB import BookDataBase, ReaderDataBase
from typing import Union


class Library:
    def __init__(self, books: list = None, readers: list = None,
                 books_data_base_path='./DB/books.json', readers_data_base_path='./DB/reader.json'):
        self.__book_db = BookDataBase(books_data_base_path)
        self.__reader_db = ReaderDataBase(readers_data_base_path)
        self.__books = books if books else self.__book_db.read_from_db()
        self.__readers = readers if readers else self.__reader_db.read_from_db()
        print(self.__readers)

    def add_book(self, title: str, author: str, year: int, book_id: int = None):
        """Добавление книги"""
        if book_id is not None:
            for book in self.__books:
                if book.get_id() == book_id:
                    print(f'Error: book with id {book_id} already exists')
                    return 'Error: book with this id already exists'

        self.__books.append(Book(title, author, year, book_id))
        self.save_books()
        print('Done: book was successfully added to the library')
        return 'Done'

    def add_reader(self, name: str, surname: str, patronymic: str, year: int, reader_id: int = None):
        """Добавление читателя"""
        if reader_id is not None:
            for reader in self.__readers:
                if reader.get_id() == reader_id:
                    print(f'Error: reader with id {reader_id} already exists')
                    return 'Error: reader with this id already exists'

        self.__readers.append(Reader(name, surname, patronymic, year, reader_id))
        self.save_readers()
        print(f'Done: reader was successfully added to the library')
        return 'Done'

    def del_book(self, book_id):
        book = self.get_book_by_id(book_id)
        print(book)
        if book:
            if book in self.__books:
                if not book.get_reader_id():
                    self.__books.remove(book)
                    self.save_books()
                    return 'Done'
                return 'Error, this book has reader'
            return 'Error, this book is not in the library'

    def del_reader(self, reader_id):
        reader = self.get_reader_by_id(reader_id)
        if reader:
            for book in self.__books:
                if book.get_reader_id() == reader_id:
                    return 'Error, this reader has a book'

            self.__readers.remove(reader)
            self.save_readers()
            return 'Done'
        return 'Error, this reader is not in the library'

    def save_books(self):
        self.__book_db.write_to_db(self.__books)

    def save_readers(self):
        self.__reader_db.write_to_db(self.__readers)

    def print_all_books(self):
        """Функция вывода всех книг"""
        if not self.__books:
            print('There are no books in the library yet')
            return

        for book in self.__books:
            print(book)

    def print_available_books(self):
        """Функция вывода книг доступных в библиотеке"""
        for book in self.__books:
            if not book.get_reader_id():
                print(book)

    def print_all_readers(self):
        """
        Функция вывода всех читателей
        """
        if not self.__readers:
            print('There are no readers in the library yet')
            return

        for reader in self.__readers:
            print(reader)

    def print_sorted_book(self, sort: str = 'id', reverse: bool = False):
        """
        Функция вывода отсортированого списка книг

        :param sort: по какому признаку сортируем (доступна сортировка по id - 'id',
                                                   по названию - 'title' и по году издания - 'year')
        :param reverse: False когда реверса нет, True когда он есть
        """
        if sort not in ['id', 'title', 'year']:
            print(f'Error: no sorting by {sort} field')
            return

        def get_sort_field(obj: Book):
            if sort == 'id':
                return obj.get_id()
            elif sort == 'title':
                return obj.get_title()
            elif sort == 'year':
                return obj.get_year()

        for book in sorted(self.__books, key=get_sort_field, reverse=reverse):
            print(book)

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
        print(f'Books with id {book_id} have been successfully issued to the reader with id {reader_id}')
        self.save_books()

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
        print(f'Reader {reader.get_name()} {reader.get_surname()} '
              f'returned the book "{book.get_title()}" to the library')
        self.save_books()

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

        print(f'books = {self.__books}, type = {type(self.__books)}')
        print({type(sorted(self.__books, key=get_sort_field_book, reverse=reverse))})
        books = [book for book in sorted(self.__books, key=get_sort_field_book, reverse=reverse)]
        return books, sort

    def get_readers(self, sort):
        if sort not in ['id', 'name', 'surname', 'year']:
            print(sort)
            sort = 'id'

        def get_sort_field_reader(obj: Reader):
            if sort == 'id':
                return int(obj.get_id())
            elif sort == 'name':
                print(f'name = {obj.get_name()}')
                print(f'surname = {obj.get_surname()}')
                return obj.get_name()
            elif sort == 'surname':
                return obj.get_surname()
            elif sort == 'year':
                return int(obj.get_year())

        print(f'readers = {self.__readers}, type = {type(self.__readers)}')
        readers = [reader for reader in sorted(self.__readers, key=get_sort_field_reader)]
        return [readers, sort]

    def get_book_by_id(self, book_id: int) -> Union[Book, None]:
        """
        Функция получения книги по id из списка книг

        :param book_id: id книги, которую хотим получить
        :return: obj Book (если книга есть в библиотеке); None (если книги нет)
        """
        for book in self.__books:
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
        for reader in self.__readers:
            if reader.get_id() == reader_id:
                return reader
        return None
