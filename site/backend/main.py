import os
import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from Library.library import Library
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


class UserLogin:
    """ Класс для описания пользователя, который вошел в аккаунт """
    def fromDB(self, reader_id, db: Library):
        self.__user = db.get_reader_by_id(reader_id)
        return self

    def create(self, reader):
        self.__user = reader
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.ID)


load_dotenv('.env')  # Выгружаем переменные из окружения

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

login_manager = LoginManager()
login_manager.init_app(app)  # Создаем менеджер для регистрации и входа в аккаунт пользователями

app.config['DEBUG'] = True  # Ставим DEBUG = True для тестов, потом нужно поменять на False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Выгружаем из окружения секретный ключ

lib = Library()  # Создаем экземпляр библиотеки


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, lib)  # Берем пользователя из базы данных


@app.route('/')
def index():
    """ Главная страница сайта """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя из библиотеки
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def api_login():
    """ Вход пользователя в аккаунт """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя из библиотеки

    if request.method == 'POST':
        # Обработчик POST запроса
        email = request.form.get('email')  # Получаем почту из формы
        password = request.form.get('password')  # Получаем пароль из формы

        if not email or not password:
            # Проверяем данные на валидность
            msg = 'Error: invalid data'
            return render_template('login.html', user=user, message=msg)

        user = lib.get_reader_by_email(email)
        if user and password and check_password_hash(user.password, password):  # Проверяем правильно ли введен пароль
            userlogin = UserLogin().create(user)  # Создаем объект зарегистрированного пользователя
            login_user(userlogin)
            return redirect(url_for('index'))  # После входа - переносим пользователя на главную страницу

    return render_template('login.html', user=user)


@app.route('/registration', methods=['GET', 'POST'])
def api_registration():
    """ Регистрация пользователя """
    user = lib.get_reader_by_id(current_user.get_id())

    if request.method == 'POST':
        # Обрабатываем POST запрос
        email = request.form.get('email')  # Получаем поле email из html формы
        password = request.form.get('password')  # Получаем поле password из html формы
        confirm_password = request.form.get('confirm_password')  # Получаем поле confirm_password из html формы

        name = request.form.get('name')  # Получаем поле name из html формы
        surname = request.form.get('surname')  # Получаем поле surname из html формы
        patronymic = request.form.get('patronymic')  # Получаем поле patronymic из html формы
        age = request.form.get('age')  # Получаем поле age из html формы

        if not email and password and confirm_password and name and surname and patronymic and age:
            # Проверяем данные на валидность
            msg = 'Error: invalid data'
            return render_template('registration.html', user=user, message=msg)

        if not password == confirm_password:
            # Проверяем сходство паролей
            msg = 'Error: password != confirm_password'
            return render_template('registration.html', user=user, message=msg)

        if not age.isnumeric():
            # Проверяем возраст на корректность
            msg = 'Error: year must be numeric'
            return render_template('registration.html', user=user, message=msg)

        password = generate_password_hash(password)  # Хешируем пароль

        lib.add_reader(name, surname, patronymic, int(age), False, email, password)  # Создаем пользователя в бд
        msg = 'Done: you registered successfully'
        flash(msg)
        return redirect(url_for('api_login'))  # Редиректим пользователя на страницу входа в аккаунт

    return render_template('registration.html', user=user)


@app.route('/sign_out', methods=['GET'])
@login_required
def api_sign_out():
    """ Выход из аккаунта """
    logout_user()
    flash('Вы успешно вышли из аккаунта')
    return redirect(url_for('index'))


@app.route('/books', methods=['GET'])
def api_get_all_books():
    """ Страница со списком всех книг """
    sort = request.args.get('sort')  # Получаем поле для сортировки из запроса, если оно будет
                                     # не валидным, книги будут отсортированы по id
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя, который делает запрос,
                                                        # если это гость, вернем None

    books = lib.get_books(sort=sort)  # Берем книги из бд и сортируем по параметру sort
    return render_template('books.html', books=books, user=user)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def api_add_book():
    """ Добавление книги в базу данных """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        title_book = request.form.get('title')  # Берем поле title из формы html
        author_book = request.form.get('author')  # Берем поле author из формы html
        year_book = request.form.get('year')  # Берем поле year из формы html

        if not (title_book and author_book and year_book):
            # Проверяем данные на валидность
            return render_template('add_book.html', message='Введены некорректные данные', user=user)
        if not year_book.isnumeric():
            # Проверяем что год рождения - число
            return render_template('add_book.html', message='Введен некорректный год издания', user=user)

        ret_msg = lib.add_book(title_book, author_book, int(year_book))  # Добавляем книгу в базу данных
        return render_template('add_book.html', message=ret_msg, user=user)

    return render_template('add_book.html', user=user)


@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def api_delete_book():
    """ Удаление книги из базы данных """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Обработчик POST запросов
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]  # Берем книги которые были отмечены в таблице
        if len(id_books):
            ret_msg = lib.del_books(id_books)  # Удаляем отмеченные книги, если отмечена хотя бы одна книга
            return render_template('delete_book.html', books=lib.get_books(), message=ret_msg, user=user)

    sort = request.args.get('sort')  # Берем поле для сортировки книг из запроса
    return render_template('delete_book.html', books=lib.get_books(sort=sort), user=user)


@app.route('/take_book', methods=['GET', 'POST'])
@login_required
def api_take_book():
    """ Передача книги пользователю """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Обработчик POST запросов
        reader_id = request.form.get('reader_id')  # Получаем id читателя из html формы
        if not reader_id:
            # Проверяем данные на валидность
            message = 'Error'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        if not reader_id.isnumeric():
            # Проверяем, что id - число
            message = f'Error: reader_id must be numeric'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        reader = lib.get_reader_by_id(reader_id)  # Получаем читателя из бд, None, если его не существует
        if not reader:
            # Проверяем что такой читатель существует
            message = f'Error: reader {reader_id} not found'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]  # Получаем id книг, которые передаем читателю

        if len(id_books):
            # Проверяем, что была выбрана хотя бы одна книга
            message = lib.give_books(id_books, int(reader_id))  # Передаем книги читателю
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

    sort = request.args.get('sort')  # Получаем поле для сортировки книг из запроса
    return render_template('take_book.html', books=lib.get_available_books(sort=sort), user=user)


@app.route('/return_book', methods=['GET', 'POST'])
@login_required
def api_return_book():
    """ Возврат книги от читателя - в библиотек """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Обработчик POST запросов
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]  # Получаем id книг, которые были выбраны

        if len(id_books):
            # Проверяем, что была выбрана хотя бы одна книга
            message = lib.return_books(id_books)  # Возвращаем книги в библиотеку
            return render_template('return_book.html', books=lib.get_unavailable_books(), message=message, user=user)

    sort = request.args.get('sort')  # Получаем поле для сортировки книг из запроса
    return render_template('return_book.html', books=lib.get_unavailable_books(sort=sort), user=user)


@app.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    """ Добавление администратора """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Обработчик POST запросов
        id_readers = [int(i) for i in request.form.keys() if i.isnumeric()]  # Получаем id выбранных пользователей

        if len(id_readers):
            # Проверяем, что выбран хотя бы один пользователь
            message = lib.add_admins(id_readers)  # Делаем пользователей администраторами
            return render_template('add_admin.html', readers=lib.get_readers(), message=message, user=user)

    return render_template('add_admin.html', readers=lib.get_readers(), user=user)


@app.route('/delete_admin', methods=['GET', 'POST'])
@login_required
def del_admin():
    """ Удаление администратора """
    user = lib.get_reader_by_id(current_user.get_id())  # Берем пользователя который делает запрос из бд
    if not user:
        # Проверяем, что он зарегистрирован
        return redirect(url_for('login'))

    if not user.is_admin:
        # Проверяем, что он админ
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Обработчик POST запросов
        id_readers = [int(i) for i in request.form.keys() if i.isnumeric()]  # Получаем id выбранных пользователей

        if len(id_readers):
            # Проверяем, что выбран хотя бы один пользователь
            message = lib.del_admins(id_readers)  # Убираем статус администратора у выбранных пользователей
            return render_template('delete_admin.html', readers=lib.get_admins(), message=message, user=user)

    return render_template('delete_admin.html', readers=lib.get_admins(), user=user)


if __name__ == '__main__':
    app.run(port=5000)  # Запускаем WEB сервер
