#%%
# Dependencies

# import json
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func
from flask import (
    Flask,
    render_template,
    url_for,
    jsonify,
    request,
    redirect)
from flask_cors import CORS # Development only--allow access to local and remote IP addresses
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
import json

# MySQL connection string
from config import user, password, host, port, dbname
connect_string = (f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}')

app = Flask(__name__)
CORS(app) # Development only--allow access to local and remote IP addresses

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string

db = SQLAlchemy(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/donations/', defaults={'search_term': None})
@app.route("/api/donations/<search_term>")
def donations(search_term):
    if search_term:
        results = db.session.execute(f'SELECT zipcode_5, donations_sum, donations_count FROM zipcode_donations WHERE CAND_PARTY = "{search_term}"')
    else:
        results = db.session.execute('SELECT zipcode_5, SUM(donations_sum), SUM(donations_count) FROM zipcode_donations GROUP BY zipcode_5')
    donation_data = []
    for result in results:
        donation_data.append({
            "zipcode": result[0],
            "donations_sum": float(result[1]),
            "donations_count": float(result[2])
            })
    return jsonify(donation_data)

@app.route("/api/census/<search_term>")
def census(search_term):
    results = db.session.execute(f'SELECT * FROM census_data WHERE zipcode_5 = "{search_term}"')
    census_data = []
    for result in results:
        census_data.append({
            "id": result[0],
            "zipcode": result[1],
            "pop_total": result[2],
            "unemployment_rate": result[3],
            "median_household_income": result[4],
            "healthcare_rate": result[5],
            "hs_graduation_rate": result[6],
            "assoc_degree_rate": result[7],
            "bachelor_degree_rate": result[8],
            "grad_degree_rate": result[9],
            })
    return jsonify(census_data)

@app.route("/api/parties/")
def parties():
    results = db.session.execute(f'SELECT CAND_PARTY FROM zipcode_donations GROUP BY CAND_PARTY')
    parties_list = []
    for result in results:
        parties_list.append(result[0])
    return jsonify({'parties': parties_list})

if __name__ == '__main__':
    app.run(debug=True)