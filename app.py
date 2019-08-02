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
connect_string = (f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}?use_pure=True')

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

@app.route('/api/donations/', defaults={'search_term': 'TOTAL'})
@app.route("/api/donations/<search_term>")
def donations(search_term):
    donation_results = db.session.execute(f'SELECT zd.zipcode_5, donations_sum, donations_median, donations_count, zipcode_geojson FROM zipcode_donations zd join zi_p5 on zi_p5.zipcode_5 = zd.zipcode_5 WHERE CAND_PARTY = "{search_term}"')
    maximums_results = db.session.execute(f'SELECT max(donations_sum), max(donations_median), max(donations_count) FROM zipcode_donations WHERE CAND_PARTY = "{search_term}"').first()
    features = []
    maximums = {
        "donations_sum": float(maximums_results[0]),
        "donations_median": float(maximums_results[1]),
        "donations_count": float(maximums_results[2])
    }
    for result in donation_results:
        geometry = json.loads(result[4])
        features.append({
            "type": "Feature",
            "properties": {
                "zipcode": result[0],
                "donations_sum": float(result[1]),
                "donations_median": float(result[2]),
                "donations_count": float(result[3])
            },
            "geometry": geometry
            })
    return jsonify({"type": "FeatureCollection", "features": features, "maximums": maximums})

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

@app.route("/featured")
def featured():
    return render_template("featured.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/presentation/goals")
def goals():
    return render_template("goals.html")
    
@app.route("/presentation/investors")
def investors():
    return render_template("investors.html")

@app.route("/presentation/structure")
def structure():
    return render_template("structure.html")

@app.route("/presentation/jupyter")
def jupyter():
    return render_template("jupyter.html")

@app.route("/presentation/machine_learning")
def machine_learning():
    return render_template("machine_learning.html")

@app.route("/presentation/database")
def database():
    return render_template("database.html")

@app.route("/presentation/flask_app")
def flask_app():
    return render_template("flask_app.html")

@app.route("/presentation/leaflet")
def leaflet():
    return render_template("leaflet.html")

@app.route("/presentation/conclusion")
def conclusion():
    return render_template("conclusion.html")  

@app.route("/data_walkthrough")
def data_walkthrough():
    return render_template("data_walkthrough.html")

@app.route("/data_walkthrough/acs_notebook")
def acs_notebook():
    return render_template("acs_notebook.html")

@app.route("/data_walkthrough/aws_db")
def aws_db():
    return render_template("aws_db.html")

@app.route("/data_walkthrough/fec_notebook")
def fec_notebook():
    return render_template("fec_notebook.html")

@app.route("/data_walkthrough/mysql_db")
def mysql_db():
    return render_template("mysql_db.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")




if __name__ == '__main__':
    app.run(debug=True)

# Route to render index.html template using data from Mongo
# @app.route("/")
# def render_home():
#     # Return template and data
#     return render_template("index.html")

# @app.route("/presentation.html")
# def render_presentation():
#     # Return template and data
#     return render_template("presentation.html")

if __name__ == "__main__":
    app.run(debug=True)
