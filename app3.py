# Dependencies
<<<<<<< HEAD
import json
import requests
from flask import Flask
=======

# import json
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func
# from flask import (
#     Flask,
#     render_template,
#     url_for,
#     jsonify,
#     request,
#     redirect)
from flask import Flask, render_template, redirect, jsonify
>>>>>>> e3bba6d4ff0a28235dd9cad050087f659711ff5a
from flask_cors import CORS # Development only--allow access to local and remote IP addresses
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from sqlalchemy.types import JSON

# MySQL connection string
from config import user, password, host, port, dbname
connect_string = (f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}?use_pure=True')

# Create an instance of Flask
app = Flask(__name__)
CORS(app) # Development only--allow access to local and remote IP addresses

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('index.html')

# # Build dictionary with path to geoJSON zip code data for each state
# states = {'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DC':'District of Columbia', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
# state_zip_paths = {}
# for abb, state in states.items():
#     abb = abb.lower()
#     state = state.replace(' ', '_').lower()
#     path = (f'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/{abb}_{state}_zip_codes_geo.min.json')
#     state_zip_paths.update({abb.upper(): path})
# print(state_zip_paths)

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)
=======
<<<<<<< HEAD
# Route to render index.html template using data from Mongo
@app.route("/")
def render_home():
    # Return template and data
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
=======
#%%
>>>>>>> 84feac128decfa053aa542b93bc441087ec2075e
>>>>>>> e3bba6d4ff0a28235dd9cad050087f659711ff5a
