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


# states = {'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DC':'District of Columbia', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
# state_zip_paths = {}
# for abb, state in states.items():
#     abb = abb.lower()
#     state = state.replace(' ', '_').lower()
#     path = (f'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/{abb}_{state}_zip_codes_geo.min.json')
#     state_zip_paths.update({abb.upper(): path})
#     # gdf = gpd.read_file(filename)
#     # gdf
# print(state_zip_paths['AL'])
# illinois = requests.get(state_zip_paths['IL']).json()
# print(illinois['60626'])
# gdf = gpd.read_file('zcta5.geo.json')


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON


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

# Route to render index.html template using data from Mongo
@app.route("/")
def render_home():
    # Return template and data
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
