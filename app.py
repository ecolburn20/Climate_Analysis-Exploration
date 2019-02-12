# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 13:53:26 2019

@author: Owner
"""

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
from datetime import datetime, timedelta, date

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Measurements = Base.classes.measurement
Measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    Measurements = Base.classes.measurement
    for row in session.query(Measurements.date).all():
        x = row
    enddate = x[0]
    datetime_object = datetime.strptime(enddate, '%Y-%m-%d')
    startdate = datetime_object.replace(datetime_object.year - 1)
    y = datetime.strftime(startdate, '%Y-%m-%d')
    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= y).order_by(Measurements.date).all()
    precip_data = []
    for precip in results:
        precip_dict = {precip.date:precip.prcp}
        precip_data.append(precip_dict)

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    Station = Base.classes.station
    results = session.query(Station.name).all()

   
    station_data = []
    for station in results:
    
        station_data.append(station)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    Measurements = Base.classes.measurement
    for row in session.query(Measurements.date).all():
        x = row
    enddate = x[0]
    datetime_object = datetime.strptime(enddate, '%Y-%m-%d')
    startdate = datetime_object.replace(datetime_object.year - 1)
    y = datetime.strftime(startdate, '%Y-%m-%d')

    l = []
    qry = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= y).order_by(Measurements.date).all()
    for row in qry:
        l.append(row)
    return jsonify(l)
    

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    Measurements = Base.classes.measurement
    x = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
    filter(Measurements.date >= start).all()
    start_dict = {'min':x[0][0],'average':x[0][1],'max':x[0][2]}
    return jsonify(start_dict)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    Measurements = Base.classes.measurement
    y =session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
    filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    start_end = {'min':y[0][0],'average':y[0][1],'max':y[0][2]}
    return jsonify(start_end)
    
    
from flask import request

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)