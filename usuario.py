from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask import Blueprint

usuario_rota = Blueprint('usuario', __name__)

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '13032018',
    'database': 'user_gerenciador',
}

@usuario_rota.route('/')
def landing():
    return render_template('landing.html')

@usuario_rota.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@usuario_rota.route('/lista_usuario')
def lista_usuario():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('lista_usuario.html', rows=rows)

@usuario_rota.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE nome = %s AND senha = %s", (username, password))
        user = cursor.fetchone()
        cursor.fetchall()
        cursor.close()
        db.close()

        if user:
            session['user_id'] = user['ID']
            session['username'] = user['nome']
            return redirect(url_for('usuario.dashboard'))
        else:
            flash('Falha no login, verifique seu Email e Senha, ou Registre-se.')
            return redirect(url_for('usuario.login'))

    return render_template('login.html')

@usuario_rota.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        cursor.close()
        db.close()
        flash('Registrado com sucesso!')
        return redirect(url_for('usuario.login'))

    return render_template('register.html')

@usuario_rota.route('/formulario', methods=['GET', 'POST'])
@usuario_rota.route('/formulario/<int:id>', methods=['GET', 'POST'])
def formulario(id=None):
    user = None
    if id:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE ID = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        if id:
            cursor.execute("UPDATE users SET nome = %s, email = %s, senha = %s WHERE ID = %s", (nome, email, senha, id))
            flash('Usuário atualizado com sucesso!')
        else:
            cursor.execute("INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            flash('Usuário registrado com sucesso!')
        
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('usuario.dashboard'))
    
    return render_template('formulario.html', user=user)

@usuario_rota.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'username' not in session:
        return redirect(url_for('usuario.login'))
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE ID=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('usuario.dashboard'))

@usuario_rota.route('/view/<int:id>')
def view(id):
    if 'username' not in session:
        return redirect(url_for('usuario.login'))
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE ID=%s", (id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('view_usuario.html', user=user)

@usuario_rota.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuario.landing'))

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Defina uma chave secreta para a sessão
app.register_blueprint(usuario_rota, url_prefix='/usuario')

if __name__ == '__main__':
    app.run(debug=True)
