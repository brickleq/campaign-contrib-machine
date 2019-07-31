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


class zipcode_donation(db.Model):
    __tablename__ = 'zipcode_donations'

    id = db.Column(db.Integer, primary_key=True)
    zipcode_5 = db.Column(db.Integer)
    CAND_PARTY = db.Column(db.String(10))
    donations_sum = db.Column(db.Float)
    donations_median = db.Column(db.Float)
    donations_count = db.Column(db.Integer)

    def __repr__(self):
        return '<zip %r>' % (self.zipcode_5)



# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/zip/')
@app.route("/api/zip/<search_term>")
def zip_donations_by_party():
    if search_term:
        results = db.session.query(zipcode_donation.zipcode_5,
                                zipcode_donation.CAND_PARTY,
                                zipcode_donation.donations_sum,
                                zipcode_donation.donations_median,
                                zipcode_donation.donations_count).filterby(CAND_PARTY = search_term)
    else:
        results = db.session.query(zipcode_donation.zipcode_5,
                            zipcode_donation.CAND_PARTY,
                            zipcode_donation.donations_sum,
                            zipcode_donation.donations_median,
                            zipcode_donation.donations_count).all()
    donation_data = []
    for result in results:
        donation_data.append({
            "zipcode": result[0],
            "CAND_PARTY": result[1],
            "donations_sum": result[2],
            "donations_median": result[3],
            "donations_total": result[4]
            })
    return jsonify(donation_data)


if __name__ == '__main__':
    app.run(debug=True)