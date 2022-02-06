import socket
from Networking.msgutils import send_msg, recv_msg, default_encoding
from Library.library import Library
from threading import Thread, Lock

sock = socket.socket()
sock.bind(('localhost', 5555))
sock.listen(5)


lib = Library()


def work_with_client(conn, lock):
    send_msg("""Список доступных команд:

        print_books - выводит список всех книг
        ----------------------------------------------------             
        print_readers - выводит список всех читателей                    
        ----------------------------------------------------
        add_book - добавление книги в бд
        ----------------------------------------------------
        add_reader - добавление читателя в бд
        ----------------------------------------------------
        del_book - удаление книги из бд
        ----------------------------------------------------
        del_reader - удаление читателя из бд
        ----------------------------------------------------
        give_book - передача книги к читателю
        ----------------------------------------------------
        return_book - возврат книги от читателя в библиотеку
                     """.encode(default_encoding), conn, 'statement')
    while True:
        send_msg('Введите комманду:'.encode(default_encoding), conn)  # >>
        msg, msg_type = recv_msg(conn)  # <<
        if not msg:
            conn.close()
            break
        msg = msg.decode(default_encoding)

        if msg == 'stop_server':
            send_msg('Сервер остановлен'.encode(default_encoding), conn)
            conn.close()
            return

        if msg == 'end_connection':
            send_msg('Соединение разорвано'.encode(default_encoding), conn)
            conn.close()
            break

        if msg == 'print_books':
            send_msg('Введите поле по которому хотите провести сортировку'  # >>
                     ' книг:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # <<
            msg = msg.decode(default_encoding)
            books, sort_field = lib.get_books(msg)
            if not books:
                send_msg('Книг не найдено'.encode(default_encoding), conn, 'statement')
                continue
            books = [f'{books}\n' for books in books]
            send_msg(f"Список книг отсортирован по полю {sort_field}\n{''.join(books)}".encode(default_encoding),
                     conn, 'statement')
            continue

        if msg == 'print_readers':
            send_msg('Введите поле по которому хотите провести сортировку'
                     ' читателей:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)
            msg = msg.decode(default_encoding)
            readers, sort_field = lib.get_readers(msg)
            if not readers:
                send_msg('Читателей не найдено'.encode(default_encoding), conn, 'statement')
                continue
            readers = [f'{reader}\n' for reader in readers]
            send_msg(f"Список читателей отсортирован по полю"
                     f" {sort_field}\n{''.join(readers)}".encode(default_encoding), conn, 'statement')
            continue

        if msg == 'add_book':
            send_msg('Введите название книги:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем названия книги
            title = msg.decode(default_encoding)

            send_msg('Введите автора книги:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем автора книги
            author = msg.decode(default_encoding)

            send_msg('Введите год издания книги:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем год издания книги
            year_of_publishing = msg.decode(default_encoding)
            if not year_of_publishing.isnumeric:
                send_msg('Ошибка, год издания должен быть числом'.encode(default_encoding), conn)
                continue
            year_of_publishing = int(year_of_publishing)

            lock.acquire()
            ret = lib.add_book(title, author, year_of_publishing)
            lock.release()
            if ret == 'Error: book with this id already exists':
                send_msg('Произошла ошибка, id уже занят, попробуйте снова'
                         ''.encode(default_encoding), conn, 'statement')
                continue
            send_msg('Книга успешно добавлена'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'add_reader':
            send_msg('Введите имя читателя:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем имя читателя
            name = msg.decode(default_encoding)

            send_msg('Введите фамилию читателя:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем фамилию читателя
            surname = msg.decode(default_encoding)

            send_msg('Введите отчество читателя:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем отчество читателя
            patronymic = msg.decode(default_encoding)

            send_msg('Введите возраст читателя:'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем год рождения читателя
            age = msg.decode(default_encoding)

            if not age.isnumeric:
                send_msg('Ошибка, возраст должен быть числом'.encode(default_encoding), conn, 'statement')
                continue
            age = int(age)

            lock.acquire()
            ret = lib.add_reader(name, surname, patronymic, age)
            lock.release()
            if ret == 'Error: reader with this id already exists':
                send_msg('Ошибка, читатель с таким id уже существует'.encode(default_encoding), conn, 'statement')
                continue

            send_msg('Читатель успешно добавлен'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'del_book':
            send_msg('Введите id книги, которую хотите удалить'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id книги
            _id = msg.decode(default_encoding)

            if _id.isnumeric():
                _id = int(_id)
            else:
                send_msg('Ошибка, id должен быть числом'.encode(default_encoding), conn, 'statement')
                continue

            ret = lib.del_book(_id)
            if ret == 'Error, this book is not in the library':
                send_msg('Книги с таким id не найдено'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error, this book has reader':
                send_msg('Нельзя удалить книгу которая находится у читателя'.encode(default_encoding),
                         conn, 'statement')
                continue

            send_msg('Книга успешно удалена'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'del_reader':
            send_msg('Введите id читателя, которого хотите удалить'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id читателя
            _id = msg.decode(default_encoding)

            if not _id.isnumeric():
                send_msg('id должен быть числом'.encode(default_encoding), conn, 'statement')
                continue

            _id = int(_id)
            lock.acquire()
            ret = lib.del_reader(_id)
            lock.release()
            if ret == 'Error, this reader has a book':
                send_msg('Произошла ошибка, невозможно удалить читателя. Читатель имеет'
                         ' на руках книгу'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error, this reader is not in the library':
                send_msg('Читателя с таким id не найдено'.encode(default_encoding), conn, 'statement')
                continue

            send_msg('Читателя успешно удален'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'give_book':
            send_msg('Введите id читателя, которому хотите отдать книгу'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id читателя
            reader_id = msg.decode(default_encoding)

            send_msg('Введите id книги, которую хотите отдать читателю'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id книги
            book_id = msg.decode(default_encoding)

            if not reader_id.isnumeric() and book_id.isnumeric():
                send_msg('Ошибка, id книги/читателя не являются числом'.encode(default_encoding), conn, 'statement')
                continue

            reader_id = int(reader_id)
            book_id = int(book_id)

            ret = lib.give_book(book_id, reader_id)
            if ret == 'Error: book with this id is not in the library':
                send_msg('Ошибка, книги с таким id нет в библиотеке'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error: reader with this id is not in the library':
                send_msg('Ошибка, читателя с таким id нет в библиотеке'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error: book with this id are out of stock':
                send_msg('Ошибка, книга с таким id находится у другого читателя'.encode(default_encoding),
                         conn, 'statement')
                continue

            send_msg('Книга успешно передана читателю'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'return_book':
            send_msg('Введите id читателя, у которого хотите забрать книгу'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id читателя
            reader_id = msg.decode(default_encoding)

            send_msg('Введите id книги, которую хотите забрать у читателя'.encode(default_encoding), conn)
            msg, msg_type = recv_msg(conn)  # получаем id книги
            book_id = msg.decode(default_encoding)

            if not reader_id.isnumeric() and book_id.isnumeric():
                send_msg('Ошибка, id книги/читателя не являются числом'.encode(default_encoding), conn, 'statement')
                continue

            reader_id = int(reader_id)
            book_id = int(book_id)

            lock.acquire()
            ret = lib.return_book(book_id, reader_id)
            lock.release()
            if ret == 'Error: book with this id is not in the library':
                send_msg('Ошибка, книги с таким id нет в библиотеке'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error: reader with this id is not in the library':
                send_msg('Ошибка, читателя с таким id нет в библиотеке'.encode(default_encoding), conn, 'statement')
                continue

            if ret == 'Error: book with this id is not in the possession of the reader':
                send_msg('Ошибка, эта книга находится не у этого читателя'.encode(default_encoding),
                         conn, 'statement')
                continue

            send_msg('Книга успешно передана в библиотеку'.encode(default_encoding), conn, 'statement')
            continue

        if msg == 'test':
            send_msg('Тестовое сообщение'.encode(default_encoding), conn, 'statement')
            continue

        send_msg('Неизвестная команда'.encode(default_encoding), conn, 'statement')


def start_server():
    lock = Lock()
    while True:
        conn, _ = sock.accept()
        thread = Thread(target=work_with_client, args=(conn, lock))
        thread.start()


start_server()
sock.close()
