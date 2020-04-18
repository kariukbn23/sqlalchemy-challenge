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

    #Query of prcp data for year that will include the date, prcp and station id 
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


@app.route('/api/v1.0/datesearch/StartDate')
def start(StartDate):
    select = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    responses4 =  (session.query(*select).filter(func.strftime("%Y-%m-%d", Measurement.date) >= StartDate).group_by(Measurement.date).all())

    Dates_Data = []                       
    for response in responses4:
        Dates_dictionary = {}
        Dates_dictionary["date"] = response[0]
        Dates_dictionary["low_temp"] = response[1]
        Dates_dictionary["average_temp"] = response[2]
        Dates_dictionary["high_temp"] = response[3]
        Dates_Data.append(Dates_dictionary)
    return jsonify(Dates_Data)

@app.route('/api/v1.0/datesearch/StartEndDate')
def StartEnd(StartDate, EndDate):
    select2 = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    responses5 =  (session.query(*select2).filter(func.strftime("%Y-%m-%d", Measurement.date) >= StartDate).filter(func.strftime("%Y-%m-%d", Measurement.date) <= EndDate).group_by(Measurement.date).all())

    Dates_Data2 = []                       
    for response in responses5:
        Dates_dictionary2 = {}
        Dates_dictionary2["date"] = response[0]
        Dates_dictionary2["low_temp"] = response[1]
        Dates_dictionary2["average_temp"] = response[2]
        Dates_dictionary2["high_temp"] = response[3]
        Dates_Data2.append(Dates_dictionary2)
    
    return jsonify(Dates_Data2)

if __name__ == '__main__':
    app.run(debug=True)


