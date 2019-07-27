# Dependencies

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
from flask import Flask
from flask_cors import CORS # Development only--allow access to local and remote IP addresses
from flask_sqlalchemy import SQLAlchemy

# MySQL connection string
from config import user, password, host, port, dbname
connect_string = f('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}')

# Create an instance of Flask
app = Flask(__name__)
CORS(app) # Development only--allow access to local and remote IP addresses

app.config['SQLALCHEMY_DATABASE_URI'] = connect_string
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)