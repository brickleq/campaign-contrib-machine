import geopandas as gpd 
import json
import requests

# Build dictionary with path to geoJSON zip code data for each state
# states = {'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DC':'District of Columbia', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
# state_zip_paths = {}
# for abb, state in states.items():
#     abb = abb.lower()
#     state = state.replace(' ', '_').lower()
#     path = (f'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/{abb}_{state}_zip_codes_geo.min.json')
#     state_zip_paths.update({abb.upper(): path})
# print(state_zip_paths)

from flask import Flask, jsonify
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

class ZIP5(db.Model):
    zipcode_5 = db.Column(db.String(5), unique=True, nullable=False, primary_key=True)
    zipcode_geojson = db.Column(db.String(64000), nullable=False)

    def __repr__(self):
        return "<ZIP: {}>".format(self.title)
db.create_all()

abb = 'il'
state = 'illinois'
path = ('https://github.com/jgoodall/us-maps/blob/master/geojson/zcta5.geo.json?raw=true')
USA = requests.get(path).json()
for feature in USA['features']:
    zip_code = feature['properties']['ZCTA5CE10']
    feature_geojson = feature
    try:
        entry = ZIP5(zipcode_5 = zip_code, zipcode_geojson = json.dumps(feature_geojson))
        db.session.add(entry)
        db.session.commit()
        print('Success posting record for ZIP ' + zip_code)
    except:
        print('An error occurred posting record for ZIP ' + zip_code)
# print(illinois)
# for 
# us_zips = requests.get('https://raw.githubusercontent.com/jgoodall/us-maps/master/geojson/zcta5.geo.json').json()
# for feature in us_zips:
#     print(feature)
    # zip_code = feature['features']['properties']['ZCTA5CE10']
    # feature_geojson = feature

if __name__ == '__main__':
    app.run(debug=True)