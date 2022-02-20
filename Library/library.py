from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from Library.DataBase.DataBase import DataBaseSQLAlchemy


class Library:
    def __init__(self):
        self.__data_base = DataBaseSQLAlchemy()

    def add_book(self, title: str, author: str, year: int):
        """Добавление книги"""
        self.__data_base.add_book(Book(None, title, author, year))
        print('Done: book was successfully added to the library')
        return 'Done'

    def add_reader(self, name: str, surname: str, patronymic: str, age: int):
        """Добавление читателя"""
        self.__data_base.add_reader(Reader(None, name, surname, patronymic, age))
        print(f'Done: reader was successfully added to the library')
        return 'Done'

    def del_book(self, book_id):
        book = self.__data_base.get_book(book_id)
        if book:
            if not book.reader():
                self.__data_base.delete_book(book)
                return 'Done'
            return 'Error, this book has reader'
        return 'Error, this book is not in the library'

    def del_reader(self, reader_id):
        reader = self.__data_base.get_reader(reader_id)
        if reader:
            for book in self.__data_base.get_books():
                if book.reader_id() == reader_id:
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
        book = self.__data_base.get_book(book_id)
        if not book:
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.__data_base.get_reader(reader_id)
        if not reader:
            print(f'Error: reader with id {reader_id} is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.reader_id is not None:
            print(f'Error: book with id {book_id} are out of stock')
            return 'Error: book with this id are out of stock'

        book.reader_id = reader_id
        self.__data_base.update_book(book)

    def return_book(self, book_id: int, reader_id: int):
        """
        Функция возврата книги библиотеку

        :param book_id: id книги, которую возвращаем
        :param reader_id: id читателя, который возвращает книгу
        """
        book = self.__data_base.get_book(book_id)
        if not book:
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.__data_base.get_reader(reader_id)
        if not reader:
            print(f'Error: reader with this id is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.get_reader != reader.ID:
            print(f'Error: book with this id is not '
                  f'in the possession of the reader'
                  f'{reader.get_name()} {reader.get_surname()}')
            return 'Error: book with this id is not in the possession of the reader'

        book.reader_id = None
        self.__data_base.update_book(book)

    def get_books(self, sort: str = 'id', reverse: bool = False):
        if sort not in ['id', 'title', 'author', 'year']:
            sort = 'id'

        def get_sort_field_book(obj: Book):
            if sort == 'id':
                return int(obj.ID)
            elif sort == 'title':
                return obj.title
            elif sort == 'author':
                return obj.author
            elif sort == 'year':
                return int(obj.year)

        books = [book for book in sorted(self.__data_base.get_books(), key=get_sort_field_book, reverse=reverse)]
        return books, sort

    def get_readers(self, sort):
        if sort not in ['id', 'name', 'surname', 'year']:
            print(sort)
            sort = 'id'

        def get_sort_field_reader(obj: Reader):
            if sort == 'id':
                return int(obj.ID)
            elif sort == 'name':
                return obj.name
            elif sort == 'surname':
                return obj.surname
            elif sort == 'year':
                return int(obj.age)

        readers = [reader for reader in sorted(self.__data_base.get_readers(), key=get_sort_field_reader)]
        return [readers, sort]
