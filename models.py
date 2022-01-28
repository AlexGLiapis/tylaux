from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# In order to run, worddb database must be created in postgres
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_STRING",'postgres://postgres:password@localhost:5432/worddb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={'autocommit': False})

class Word(db.Model):
    __tablename__ = 'Word'

    word_id = db.Column(db.Integer, primary_key = True, index = True)
    word_value = db.Column(db.String(80), index = True)
    word_length = db.Column(db.Integer, index = True)
    word_type = db.Column(db.String(80))
    word_description = db.Column(db.String(320))

db.drop_all()
db.create_all()
