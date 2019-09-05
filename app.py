from flask import (
    Flask,
    render_template,
    url_for,
    jsonify,
    request,
    redirect)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
import json

app = Flask(__name__)

#################################################
# Database Setup
#################################################

connect_string = 'sqlite:///db/donations_db.db'
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string
db = SQLAlchemy(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/donations/', defaults={'search_term': 'TOTAL'})
@app.route("/api/donations/<search_term>")
def donations(search_term):
    donation_results = db.session.execute(f'SELECT zd.zipcode_5, donations_sum, donations_median, donations_count, zipcode_geojson, sum_DEM_quartile, sum_DEM_predicted, sum_REP_quartile, sum_REP_predicted FROM zipcode_donations zd join zi_p5 on zi_p5.zipcode_5 = zd.zipcode_5 join zipcodes_quartiles zq on zq.zipcode_5 = zd.zipcode_5 WHERE CAND_PARTY = "{search_term}"')
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
                "donations_count": float(result[3]),
                "actual_DEM_quartile": int(result[5]),
                "predicted_DEM_quartile": int(result[6]),
                "actual_REP_quartile": int(result[7]),
                "predicted_REP_quartile": int(result[8]),
                "difference_DEM": 3 + int(result[5]) - int(result[6]),
                "difference_REP": 3 + int(result[7]) - int(result[8])
            },
            "geometry": geometry
            })
    return jsonify({"type": "FeatureCollection", "features": features, "maximums": maximums})

def census_request(search_term):
    result = db.session.execute(f'SELECT * FROM census_data WHERE zipcode_5 = "{search_term}"').first()
    census_data = {
        "id": result[0],
        "zipcode": result[1],  
        "pop_total": f'{result[2]:,}',
        "unemployment_rate": round(result[3] * 100, 1),
        "median_household_income": f'{round(result[4]):,}',
        "healthcare_rate": round(result[5] * 100, 1),
        "hs_graduation_rate": round(result[6] * 100, 1),
        "assoc_degree_rate": round(result[7] * 100, 1),
        "bachelor_degree_rate": round(result[8] * 100, 1),
        "grad_degree_rate": round(result[9] * 100, 1)
        }
    return census_data

def quartile_request(search_term):
    quartile_result = db.session.execute(f'SELECT * FROM zipcodes_quartiles WHERE zipcode_5 = "{search_term}"').first()
    quartile_data = {
        "actual_DEM_quartile": int(quartile_result[1]),
        "actual_REP_quartile": int(quartile_result[2]),
        "predicted_DEM_quartile": int(quartile_result[5]),
        "predicted_REP_quartile": int(quartile_result[6])
        }
    return quartile_data

@app.route("/api/census/<zipcode>")
def census(zipcode):
    result = census_request(zipcode)
    result.update(quartile_request(zipcode))
    print(result)
    return jsonify([result])

@app.route("/api/zipcodes/")
def zipcode_list():
    results = db.session.execute(f'SELECT DISTINCT(zipcode_5) FROM zipcode_donations ORDER BY zipcode_5 ASC')
    zipcode_list = []
    for result in results:
        zipcode_list.append(result[0])
    return jsonify({'zipcodes': zipcode_list})


@app.route("/api/zipcode_geo/<zipcode>")
def zipcode_geo(zipcode):
    donation_results = db.session.execute(f'SELECT zd.zipcode_5, donations_sum, donations_median, donations_count, zipcode_geojson FROM zipcode_donations zd join zi_p5 on zi_p5.zipcode_5 = zd.zipcode_5 WHERE zd.zipcode_5="{zipcode}" and party="TOTAL"')
    features = []
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
    return jsonify({"type": "FeatureCollection", "features": features})


@app.route("/api/parties/")
def parties():
    results = db.session.execute(f'SELECT DISTINCT(CAND_PARTY) FROM zipcode_donations')
    parties_list = []
    for result in results:
        parties_list.append(result[0])
    return jsonify({'parties': parties_list})

@app.route("/zipcode/<zipcode>")
def zipcode_profile(zipcode):
    result = census_request(zipcode)
    result.update(quartile_request(zipcode))
    return render_template("zip_code.html", data=result)
    
@app.route("/featured")
def featured():
    return render_template("featured.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/goals")
def goals():
    return render_template("/presentation/goals.html")
    
@app.route("/investors")
def investors():
    return render_template("/presentation/investors.html")

@app.route("/structure")
def structure():
    return render_template("/presentation/structure.html")

@app.route("/jupyter")
def jupyter():
    return render_template("/presentation/jupyter.html")

@app.route("/machine_learning")
def machine_learning():
    return render_template("/presentation/machine_learning.html")

@app.route("/database")
def database():
    return render_template("/presentation/database.html")

@app.route("/flask_app")
def flask_app():
    return render_template("/presentation/flask_app.html")

@app.route("/leaflet")
def leaflet():
    return render_template("/presentation/leaflet.html")

@app.route("/conclusion")
def conclusion():
    return render_template("/presentation/conclusion.html")  

@app.route("/data_walkthrough")
def data_walkthrough():
    return render_template("data_walkthrough.html")

@app.route("/acs_notebook")
def acs_notebook():
    return render_template("/data_walkthrough/acs_notebook.html")

@app.route("/aws_db")
def aws_db():
    return render_template("/data_walkthrough/aws_db.html")

@app.route("/fec_notebook")
def fec_notebook():
    return render_template("/data_walkthrough/fec_notebook.html")

@app.route("/mysql_db")
def mysql_db():
    return render_template("/data_walkthrough/mysql_db.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

if __name__ == "__main__":
    app.run(debug=True)
