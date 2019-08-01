import geopandas as gpd 
import json
import pandas as pd
import requests
from flask import Flask, jsonify
from flask_cors import CORS # Development only--allow access to local and remote IP addresses
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from sqlalchemy.types import JSON

# MySQL connection string
from config import user, password, host, port, dbname
connect_string = (f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}')

# Create an instance of Flask
app = Flask(__name__)
CORS(app) # Development only--allow access to local and remote IP addresses

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string

db = SQLAlchemy(app)

class contributions3(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key = True)
    CMTE_ID = db.Column(db.String(16))
    TRANSACTION_PGI = db.Column(db.String(16))
    ZIP_CODE = db.Column(db.String(9))
    TRANSACTION_DT = db.Column(db.String(16))
    TRANSACTION_AMT = db.Column(db.Float)
    SUB_ID = db.Column(db.String(19))
    zipcode_5 = db.Column(db.String(16), nullable=False)
    CAND_ID = db.Column(db.String(16), nullable=True)
    CAND_PARTY = db.Column(db.String(16), nullable=True)

    def __repr__(self):
        return "<contributions3: {}>".format(self.__main__)
db.create_all()

df = pd.read_csv('contributions.csv',delimiter=',',encoding='utf-8')
print(df.head())
for i in range(len(df)):
    post = contributions2(
    CMTE_ID = df.loc[i, 'CMTE_ID'],
    TRANSACTION_PGI = df.loc[i, 'TRANSACTION_PGI'],
    ZIP_CODE = df.loc[i, 'TRANSACTION_PGI'],
    TRANSACTION_DT = df.loc[i, 'TRANSACTION_DT'],
    TRANSACTION_AMT = df.loc[i, 'TRANSACTION_AMT'],
    SUB_ID = df.loc[i, 'SUB_ID'],
    zipcode_5 = df.loc[i, 'zipcode_5'],
    CAND_ID = df.loc[i, 'CAND_ID'],
    CAND_PARTY = df.loc[i, 'CAND_PARTY'])
    try:
        db.session.add(post)
        db.session.commit()
        print('Success posting record for SUB_ID ' + str(i+1))
    except:
        print('ERROR posting record for SUB_ID ' + str(i+1))

if __name__ == "__main__":
    app.run(debug=True)