import os
import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from Library.library import Library
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


class UserLogin:
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


load_dotenv('.env')

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

CURRENT_USER_ID = 1

login_manager = LoginManager()
login_manager.init_app(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

lib = Library()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, lib)  # Берем пользователя из базы данных


@app.route('/')
def index():
    user = lib.get_reader_by_id(current_user.get_id())
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def api_login():
    user = lib.get_reader_by_id(current_user.get_id())

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(email)
        print(password)

        if not email or not password:
            msg = 'Error: invalid data'
            return render_template('login.html', user=user, message=msg)

        user = lib.get_reader_by_email(email)
        if user and password and check_password_hash(user.password, password):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))

    return render_template('login.html', user=user)


@app.route('/registration', methods=['GET', 'POST'])
def api_registration():
    user = lib.get_reader_by_id(current_user.get_id())

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        age = request.form.get('age')
        print(email)
        print(password)
        print(confirm_password)
        print()
        print(name)
        print(surname)
        print(patronymic)
        print(age)

        if not email and password and confirm_password and name and surname and patronymic and age:
            msg = 'Error: invalid data'
            return render_template('registration.html', user=user, message=msg)

        if not password == confirm_password:
            msg = 'Error: password != confirm_password'
            return render_template('registration.html', user=user, message=msg)

        if not age.isnumeric():
            msg = 'Error: year must be numeric'
            return render_template('registration.html', user=user, message=msg)

        password = generate_password_hash(password)
        print(password)

        lib.add_reader(name, surname, patronymic, int(age), False, email, password)
        msg = 'Done: you registered successfully'
        flash(msg)
        return redirect(url_for('api_login'))

    return render_template('registration.html', user=user)


@app.route('/sign_out', methods=['GET'])
@login_required
def api_sign_out():
    logout_user()
    flash('Вы успешно вышли из аккаунта')
    return redirect(url_for('index'))


@app.route('/books', methods=['GET'])
def api_get_all_books():
    sort = request.args.get('sort')
    user = lib.get_reader_by_id(current_user.get_id())

    books = lib.get_books(sort=sort)
    return render_template('books.html', books=books, user=user)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def api_add_book():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title_book = request.form.get('title')
        author_book = request.form.get('author')
        year_book = request.form.get('year')

        if not (title_book and author_book and year_book):
            return render_template('add_book.html', message='Введены некорректные данные', user=user)
        if not year_book.isnumeric():
            return render_template('add_book.html', message='Введен некорректный год издания', user=user)

        ret_msg = lib.add_book(title_book, author_book, int(year_book))
        return render_template('add_book.html', message=ret_msg, user=user)

    return render_template('add_book.html', user=user)


@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def api_delete_book():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]
        print(f'id_books = {id_books}')
        if len(id_books):
            ret_msg = lib.del_books(id_books)
            return render_template('delete_book.html', books=lib.get_books(), message=ret_msg, user=user)

    sort = request.args.get('sort')
    return render_template('delete_book.html', books=lib.get_books(sort=sort), user=user)


@app.route('/take_book', methods=['GET', 'POST'])
@login_required
def api_take_book():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        reader_id = request.form.get('reader_id')
        if not reader_id:
            message = 'Error'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        if not reader_id.isnumeric():
            message = f'Error: reader_id must be numeric'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        reader = lib.get_reader_by_id(reader_id)
        print(reader)
        if not reader:
            message = f'Error: reader {reader_id} not found'
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            message = lib.give_books(id_books, int(reader_id))
            return render_template('take_book.html', books=lib.get_available_books(), message=message, user=user)

    sort = request.args.get('sort')
    return render_template('take_book.html', books=lib.get_available_books(sort=sort), user=user)


@app.route('/return_book', methods=['GET', 'POST'])
@login_required
def api_return_book():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            message = lib.return_books(id_books)
            return render_template('return_book.html', books=lib.get_unavailable_books(), message=message, user=user)

    sort = request.args.get('sort')
    return render_template('return_book.html', books=lib.get_unavailable_books(sort=sort), user=user)


@app.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_readers = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_readers):
            message = lib.add_admins(id_readers)
            return render_template('add_admin.html', readers=lib.get_readers(), message=message, user=user)

    return render_template('add_admin.html', readers=lib.get_readers(), user=user)


@app.route('/delete_admin', methods=['GET', 'POST'])
@login_required
def del_admin():
    user = lib.get_reader_by_id(current_user.get_id())
    if not user:
        return redirect(url_for('login'))

    if not user.is_admin:
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_readers = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_readers):
            message = lib.del_admins(id_readers)
            return render_template('delete_admin.html', readers=lib.get_admins(), message=message, user=user)

    return render_template('delete_admin.html', readers=lib.get_admins(), user=user)


if __name__ == '__main__':
    app.run(port=5001)
