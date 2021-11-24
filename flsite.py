import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase



DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'jknlkmvlfndfjvbdhvhggv'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
#Вспомогательная функция для создания таблицы Базы Данных
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
#Соединение с Базой Данных, елси оно еще не установлено
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

app.config['SECRET_KEY'] = 'jknlkmvlfndfjvbdhvhggv'

menuApp = [{'name': 'Установка', 'url': 'install-flask'},
           {'name': 'Первое приложение', 'url': 'first-app'},
           {'name': 'Обратная связь', 'url': 'contact'},
           {'name': 'Вход', 'url': 'login'}]

@app.teardown_appcontext
def close_db(error):
#Закрытие соединения с Базой Данных, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu())

@app.route("/add_post", methods=["POST","GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


#
# @app.route("/about")
# def about():
#     print(url_for('about'))
#     return render_template('about.html', title="О сайте",  menu=menuApp)
#
# @app.route("/profile/<path:username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Пользователь: {username}"
#
# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         if len(request.form["username"]) > 2:
#             flash('Сообщение отправлено', category='success')
#         elif len(request.form["email"]) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#
#     return render_template('contact.html', title='Обратная связь', menu=menuApp)
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page404.html', title="Страница не найдена", menu=menuApp), 404
#
# @app.route("/login", methods=["POST","GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == "selfname" and request.form['psw'] == "123":
#         session['userLogged'] = request.form['username']
#         flash('Успешный вход', category='success')
#         return redirect(url_for('profile', username=session['userLogged']))
#     else:
#         flash('Вход не выполнен', category='error')
#     return render_template('login.html', title="Авторизация", menu=menuApp)
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username="selfedu"))




if __name__=="__main__":
    app.run(debug=True)