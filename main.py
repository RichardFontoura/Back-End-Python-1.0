from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import mysql.connector


def create_db_connection():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1111',
        database='1111'
    )
    return db


def execute_query(query, values=None, fetch=False):
    db = create_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    
    db.commit()
    cursor.close()
    db.close()
    
    return result


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('senha')
        concordo = request.form.get('concordo')

        query = "INSERT INTO teste_python (username, email, senha) VALUES (%s, %s, %s)"
        values = (username, email, senha)
        execute_query(query, values)

        print("Dados registrados com sucesso!")

    return render_template('index.html')


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    query = "SELECT * FROM teste_python WHERE email = %s AND senha = %s"
    values = (email, senha)
    result = execute_query(query, values, fetch=True)

    if result:
        session['logged_in'] = True
        session['username'] = result[0][1]
        print("Login bem-sucedido!")
        return redirect(url_for('views.logged_in'))
    else:
        print("Falha no login!")
        return redirect(url_for('views.home'))


@views.route('/logado')
def logged_in():
    if session.get('logged_in'):
        username = session.get('username')
        return render_template('logado.html', username=username)
    else:
        return redirect(url_for('views.home'))


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('views.home'))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'teste'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)