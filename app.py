#Import Necessary Dependencies 

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

import numpy as np
import pandas as pd
import datetime as dt

#Establish and create engine to link to data

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Engage ORM by reflecting tables into new model 

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#Save references to db 

Station = Base.classes.station
Measurement = Base.classes.measurement

#Create session link that connects python to db 

session = Session(engine)

#Flask app and individual routes set up

app = Flask(__name__)

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/datesearch/StartDate<br/>"
    "/api/v1.0/datesearch/StartEndDate<br/>")

@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    #Variables come from my ipynb file that includes how this data was queried right before stored as pd data frame
    LastDate = session.query(func.max(Measurement.date)).all()
    LastDate = list(np.ravel(LastDate))[0]
    LastDate = dt.datetime.strptime(LastDate, "%Y-%m-%d")
    LastMonth = int(dt.datetime.strftime(LastDate, "%m"))
    LastDay = int(dt.datetime.strftime(LastDate, "%d"))
    LastYear = int(dt.datetime.strftime(LastDate, "%Y"))
    year_ago_date = dt.date(LastYear, LastMonth, LastDay) - dt.timedelta(days=365)
    year_ago_date = dt.datetime.strftime(year_ago_date, '%Y-%m-%d')

    #Query of prcp data for year that will include the data, prcp and station id 
    responses1 = (session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date >= year_ago_date).order_by(Measurement.date).all())
    
    #Creation of open list to store data 
    Precipitation_Data = []

    #For Loop to store the desired responses to then print in json later
    for response in responses1:
        Precipitation_dictionary = {response.date: response.prcp, "Station": response.station}
        Precipitation_Data.append(Precipitation_dictionary)

    return jsonify(Precipitation_Data)


@app.route("/api/v1.0/stations")
def stations():
    responses2 = session.query(Station.name).all()
    total_stations = list(np.ravel(responses2))
    return jsonify(total_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    
    #Refer to coding rationale in the prcp route

    LastDate = session.query(func.max(Measurement.date)).all()
    LastDate = list(np.ravel(LastDate))[0]
    LastDate = dt.datetime.strptime(LastDate, "%Y-%m-%d")
    LastMonth = int(dt.datetime.strftime(LastDate, "%m"))
    LastDay = int(dt.datetime.strftime(LastDate, "%d"))
    LastYear = int(dt.datetime.strftime(LastDate, "%Y"))
    year_ago_date = dt.date(LastYear, LastMonth, LastDay) - dt.timedelta(days=365)
    year_ago_date = dt.datetime.strftime(year_ago_date, '%Y-%m-%d')
    
    
    responses3 = (session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date > year_ago_date).order_by(Measurement.date).all())

    Temperature_Data = []
    for response in responses3:
        Temperature_dictionary = {response.date: response.tobs, "Station": response.station}
        Temperature_Data.append(Temperature_dictionary)

    return jsonify(Temperature_Data)

if __name__ == '__main__':
    app.run(debug=True)


