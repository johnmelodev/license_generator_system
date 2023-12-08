from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criar um API flask
app = Flask(__name__)
# Criar um instância de SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323f#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db: SQLAlchemy


class Usuario(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)


class Licenca(db.Model):
    __tablename__ = 'licenca'
    licenca = db.Column(db.String, primary_key=True)


def inicializar_banco():
    # Executar o comando para criar o banco de dados
    db.drop_all()
    db.create_all()
    # Criar usuários administradores
    autor = Usuario(nome='joao', email='joaomelo@email.com',
                    senha='F#$¨GJgf5432j7', admin=True)
    db.session.add(autor)
    db.session.commit()


if __name__ == "__main__":
    inicializar_banco()
