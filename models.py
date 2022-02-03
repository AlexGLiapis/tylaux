from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

# Load and clean up the raw English dictionary csv & adding length column.
# Credit for English dictionary .csv goes to https://github.com/karthikramx/snippable-dictionary
df = pd.read_csv('data/dictionary.csv')
df.pop("Unnamed: 0") # Remove old indexing column.
df.rename(columns={"word":"Value", "wtype":"Type", "meaning":"Description"}, inplace=True) # Rename columns.
df['Length'] = df.apply(lambda x: len(str(x['Value'])), axis = 1) # Compute word length.
df = df[df.Length < 13] # Don't need super long words.
df['Value'] = df['Value'].str.lower() # Lowercase letters.
df = df[df.Value.str.match('^[a-z]+$') > 0] # No dashes, spaces, symbols, etc.
df.sort_values(['Length', 'Value'], inplace=True) # Sort by length to make it simpler to process.
df.reset_index(drop=True, inplace=True) # Update the index to this new ordering.

# Requires lauching psql to create "worddb" database manually
psql_str = 'postgresql://postgres:admin@localhost:5432/worddb'
engine = create_engine(psql_str, echo = False)
df.to_sql('worddb', engine, if_exists='replace')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = psql_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={'autocommit': False})

class Word(db.Model):
    __tablename__ = 'Word'

    Index = db.Column(db.Integer, primary_key = True, index = True)
    Value = db.Column(db.String(80))
    Type = db.Column(db.String(80))
    Description = db.Column(db.String(320))
    Length = db.Column(db.Integer)
