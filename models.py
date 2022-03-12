from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

app = Flask(__name__)
psql_str = 'postgresql://postgres:admin@localhost:5432/worddb'
app.config['SQLALCHEMY_DATABASE_URI'] = psql_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={'autocommit': True})
# Original Wordle answers & guesses from: https://github.com/AllValley/WordleDictionary

# Loads American English dictionary. Source: https://github.com/karthikramx/snippable-dictionary
# Does not contain variants of words, just base word (ex. silk -> silks, silky).
def load_english_dict():
    df = pd.read_csv('data/dictionary.csv')
    df.pop("Unnamed: 0") # Remove index column.
    df.pop("meaning")    # Remove meaning column.
    df.pop("wtype")      # Remove word type column.
    df.rename(columns={"word":"Value"}, inplace=True) # Rename columns.
    df['Length'] = df.apply(lambda x: len(str(x['Value'])), axis = 1) # Compute word length.
    df = df[df.Length < 11] # Don't need super long words.
    df['Value'] = df['Value'].str.lower() # Lowercase letters.
    df = df[df.Value.str.match('^[a-z]+$') > 0] # No spaces or symbols.
    df.sort_values(['Length', 'Value'], inplace=True) # Sort by length.
    df.reset_index(drop=True, inplace=True) # Update the index to new ordering
    df["Index"] = df.index # Add index column for psql later.

    # Requires lauching psql to create "worddb" database manually
    engine = create_engine(psql_str, echo = False)
    engine.execute("CREATE SCHEMA IF NOT EXISTS Word;") # Create schema.
    df.to_sql('Word', engine, if_exists='replace') # Create table.

    return True

# Loads British English full dictionary. Source: https://github.com/powerlanguage/word-lists
# Contains variants of each word, i.e. plural, possessive, etc.
# Contains many obscure words.
def load_alternate_dict():
    df = pd.read_csv("data/word-list-raw.txt", sep=":", engine="python")
    df['Length'] = df.apply(lambda x: len(str(x['Value'])), axis = 1) # Compute word length.
    df = df[df.Length < 11] # Don't need super long words.
    df['Value'] = df['Value'].str.lower() # Lowercase letters.
    df = df[df.Value.str.match('^[a-z]+$') > 0] # No spaces or symbols.
    df.sort_values(['Length', 'Value'], inplace=True) # Sort by length.
    df.reset_index(drop=True, inplace=True) # Update the index to new ordering.
    df["Index"] = df.index # Add index column for psql later.

    # Requires lauching psql to create "worddb" database manually
    engine = create_engine(psql_str, echo = False)
    engine.execute("CREATE SCHEMA IF NOT EXISTS Word;") # Create schema.
    df.to_sql('Word', engine, if_exists='replace') # Create schema.

    return True

# Loads dictionary for only five-letter words from Wordle.
# Creates two tables, one for valid guess and other for valid answers to be used.
def load_five_letter_dict():
    return True

# TODO: Obtain 1000 (or similar number) most commonly used words for
# 4, 6, 7, 8, 9, 10 length words. Use those lists to choose the daily answer.
# TODO: Use official Wordle list for default mode of length 5.

class Word(db.Model):
    __tablename__ = 'Word'

    Index = db.Column(db.Integer, primary_key = True, index = True)
    Value = db.Column(db.String(64))
    Length = db.Column(db.Integer)

load_alternate_dict()
db.create_all()
