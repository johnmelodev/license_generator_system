# database_structure.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a Flask API
app = Flask(__name__)
# Create an instance of SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323f#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db: SQLAlchemy

class User(db.Model):
    __tablename__ = 'author'
    id_author = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)

class License(db.Model):
    __tablename__ = 'license'
    license = db.Column(db.String, primary_key=True)

def initialize_database():
    # Run the command to create the database
    db.drop_all()
    db.create_all()
    # Create admin users
    author = User(name='john', email='john@example.com', password='F#$¨GJgf5432j7', admin=True)
    db.session.add(author)
    db.session.commit()

if __name__ == "__main__":
    initialize_database()
