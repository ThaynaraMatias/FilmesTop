from filmestop import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    alugueis = db.relationship('Aluguel', backref='usuario', lazy=True)

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    sinopse = db.Column(db.Text, nullable=True)
    diretor = db.Column(db.String(100), nullable=False)
    alugueis = db.relationship('Aluguel', backref='filme', lazy=True)

class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=True)
    data_aluguel = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)