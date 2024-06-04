from flask import Flask
from rotas.Home import Home_rota
from rotas.usuario import usuario_rota

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(Home_rota)
app.register_blueprint(usuario_rota,url_prefix='/usuario')

app.run(debug=True)
