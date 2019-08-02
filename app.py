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


def census_request(search_term):
    results = db.session.execute(f'SELECT * FROM census_data WHERE zipcode_5 = "{search_term}"')
    census_data = []
    for result in results:
        census_data.append({
            "id": result[0],
            "zipcode": result[1],
            "pop_total": result[2],
            "unemployment_rate": round(result[3] * 100, 1),
            "median_household_income": result[4],
            "healthcare_rate": round(result[5] * 100, 1),
            "hs_graduation_rate": round(result[6] * 100, 1),
            "assoc_degree_rate": round(result[7] * 100, 1),
            "bachelor_degree_rate": round(result[8] * 100, 1),
            "grad_degree_rate": round(result[9] * 100, 1),
            })
    return census_data


@app.route("/api/census/<zipcode>")
def census(zipcode):
    return jsonify(census_request(zipcode))

@app.route("/api/zipcodes/")
def zipcode_list():
    results = db.session.execute(f'SELECT DISTINCT(zipcode_5) FROM zipcode_donations ORDER BY zipcode_5 ASC')
    zipcode_list = []
    for result in results:
        zipcode_list.append(result[0])
    return jsonify({'zipcodes': zipcode_list})

@app.route("/api/parties/")
def parties():
    results = db.session.execute(f'SELECT DISTINCT(CAND_PARTY) FROM zipcode_donations')
    parties_list = []
    for result in results:
        parties_list.append(result[0])
    return jsonify({'parties': parties_list})

@app.route("/zipcode/<zipcode>")
def zipcode_profile(zipcode):
    data = census_request(zipcode)
    return render_template("zip_code.html", data=data[0])
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

if __name__ == "__main__":
    app.run(debug=True)
