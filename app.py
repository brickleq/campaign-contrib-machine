#%%
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
connect_string = (f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}')
#%%
# Create an instance of Flask
app = Flask(__name__)
CORS(app) # Development only--allow access to local and remote IP addresses

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string
#%%
import geopandas as gpd
import json
import geojson
import requests
from pprint import pprint

states = {'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DC':'District of Columbia', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
'''
for abb, state in states.items():
    abb = abb.lower()
    state = state.replace(' ', '_').lower()
    path = (f'State-zip-code-GeoJSON/{abb}_{state}_zip_codes_geo.min.json')
    gdf = gpd.read_file(path)
gdf
'''
    # gdf = gpd.read_file(filename)
    # gdf
# filename = '/resources/State-zip-code-GeoJSON/de_delaware_zip_codes_geo.min.json'
# state_geojson = geojson.load('resources/State-zip-code-GeoJSON/de_delaware_zip_codes_geo.min.json')
# pprint(state_geojson)
#%%
gdf = gpd.read_file('zcta5.geo.json')
#%%
gdf

#%%
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
class ZIP(db.Model):
    ZCTA5CE10 = db.Column(db.String(5), primary_key=True)
    GEOID10 = db.Column(db.String(5))
    CLASSFP10 = db.Column(db.String(2))
    MTFCC10 = db.Column(db.String(5))
    FUNCSTAT10 = db.Column(db.String(1))
    ALAND10 = db.Column(db.Numeric)
    AWATER10 = db.Column(db.Numeric)
    INTPTLAT10 = db.Column(db.Numeric)
    INTPTLON10 = db.Column(db.Numeric)
    geometry = db.Column(db.String)

    def __repr__(self):
            return '<ZIP %r>' % self.title
            
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

#%%
