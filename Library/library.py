from Library.LibraryUnits.Book import Book
from Library.LibraryUnits.Reader import Reader
from Library.DataBase.DataBase import DataBaseSQLAlchemy


class Library:
    def __init__(self):
        self.__data_base = DataBaseSQLAlchemy()

    def add_book(self, title: str, author: str, year: int):
        """Добавление книги"""
        self.__data_base.add_book(Book(None, title, author, year))  # Добавление книги в базу данных
        print('Done: book was successfully added to the library')
        return 'Done'

    def add_reader(self, name: str, surname: str, patronymic: str, age: int, is_admin: bool, email: str, password: str):
        """
        Добавление читателя

        :param name: Имя пользователя
        :param surname: Фамилия пользователя
        :param patronymic: Отчество пользователя
        :param age: Возрас пользователя
        :param is_admin: Флаг показывающий является ли пользователь администратором
        :param email: Почта пользователя
        :param password: Пароль пользователя(Хешированый)

        """
        self.__data_base.add_reader(Reader(None, name, surname, patronymic,
                                           age, is_admin, email, password))   # Добавление читателя в базу данных
        print(f'Done: reader was successfully added to the library')
        return 'Done'

    def del_book(self, book_id: int):
        """Удаление книги"""
        book = self.__data_base.get_book(book_id)  # Берем книгу из базы данных
        if book:  # Проверяем есть ли такая книга
            if not book.reader():
                self.__data_base.delete_book(book)  # Если у книги нет читателя - удаляем её
                return 'Done'
            return 'Error, this book has reader'
        return 'Error, this book is not in the library'

    def del_reader(self, reader_id: int):
        """
        Удаление читателя

        :param reader_id: id читателя, которого удаляем
        """
        reader = self.__data_base.get_reader(reader_id)
        if reader:  # Проверяем есть ли такой пользователь в бд
            for book in self.__data_base.get_books():
                if book.reader_id() == reader_id:  # Проверяем есть ли у этого читателя книга
                    return 'Error, this reader has a book'
            self.__data_base.delete_reader(reader)  # Если не найденно не одной книги у этого читателя - удаляем его
            return 'Done'
        return 'Error, this reader is not in the library'

    def give_book(self, book_id: int, reader_id: int):
        """
        Фукция выдачи книги читателю

        :param book_id: id книги, которую возвращаем
        :param reader_id: id читателя, который возвращает книгу
        """
        book = self.__data_base.get_book(book_id)
        if not book:  # Проверяем есть ли такая книга
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.__data_base.get_reader(reader_id)
        if not reader:  # Проверяем есть ли такой читатель
            print(f'Error: reader with id {reader_id} is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.reader_id is not None:  # Проверяем есть ли у этого читателя книга
            print(f'Error: book with id {book_id} are out of stock')
            return 'Error: book with this id are out of stock'

        book.reader_id = reader_id
        self.__data_base.update_book(book)  # Обновляем reader_id у этой книги

    def return_book(self, book_id: int, reader_id: int):
        """
        Функция возврата книги библиотеку

        :param book_id: id книги, которую возвращаем
        :param reader_id: id читателя, который возвращает книгу
        """
        book = self.__data_base.get_book(book_id)
        if not book:  # Проверяем есть ли такая книга
            print(f'Error: book with id {book_id} is not in the library')
            return 'Error: book with this id is not in the library'

        reader = self.__data_base.get_reader(reader_id)
        if not reader:  # Проверяем есть ли такой читатель
            print(f'Error: reader with this id is not in the library')
            return 'Error: reader with this id is not in the library'

        if book.get_reader != reader.ID:  # Проверяем валидность данных
            print(f'Error: book with this id is not '
                  f'in the possession of the reader'
                  f'{reader.get_name()} {reader.get_surname()}')
            return 'Error: book with this id is not in the possession of the reader'

        book.reader_id = None
        self.__data_base.update_book(book)  # Обновляем reader_id у этой книги

    def get_books(self, sort: str = 'id', reverse: bool = False):
        """
        Функция которая возвращает нам список отсортированых книг

        :param sort: Поле по которому сортировать книги (id, title, author или year)
        :param reverse: Флаг, который говорит как сортировать, сначала, или с конца
        """
        if sort not in ['id', 'title', 'author', 'year']:
            sort = 'id'  # Проверяем, поле sort на валидность, если sort невалидный равняем его к id

        def get_sort_field_book(obj: Book):
            """Функция которая возвращает нам поле для сортировки"""
            if sort == 'id':
                return int(obj.ID)
            elif sort == 'title':
                return obj.title
            elif sort == 'author':
                return obj.author
            elif sort == 'year':
                return int(obj.year)

        books = [book for book in sorted(self.__data_base.get_books(),
                                         key=get_sort_field_book, reverse=reverse)]  # Сортируем книги
        return books, sort

    def get_readers(self, sort, reverse):
        """
        Функция которая возвращает нам список отсортированых книг

        :param sort: Поле по которому сортировать читателей (id, name, surname, patronymic или year)
        :param reverse: Флаг, который говорит как сортировать, сначала, или с конца
        """
        if sort not in ['id', 'name', 'surname', 'patronymic', 'year']:
            sort = 'id'  # Проверяем, поле sort на валидность, если sort невалидный равняем его к id

        def get_sort_field_reader(obj: Reader):
            """Функция которая возвращает нам поле для сортировки"""
            if sort == 'id':
                return int(obj.ID)
            elif sort == 'name':
                return obj.name
            elif sort == 'surname':
                return obj.surname
            elif sort == 'patronymic':
                return obj.surname
            elif sort == 'year':
                return int(obj.age)

        readers = [reader for reader in sorted(self.__data_base.get_readers(),
                                               key=get_sort_field_reader, reverse=reverse)]  # Сортируем читателей
        return [readers, sort]
