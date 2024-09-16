from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Adicione esta linha
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/filmes.db'
db = SQLAlchemy(app)

from filmestop import routes