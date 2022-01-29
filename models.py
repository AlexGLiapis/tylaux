from flask import Flask
from flask_sqlalchemy import sqlalchemy
import pandas as pd
import os

# In order to run, worddb database must be created in postgres
df = pd.read_csv('dictionary.csv')
df['Length'] = df.apply(lambda x: len(x['Value']), axis = 1)

# Requires lauching psql to create "worddb" database manually
engine = sqlalchemy.create_engine('postgresql://postgres:admin@localhost:5432/worddb')
df.to_sql('worddb', engine, if_exists='replace')
