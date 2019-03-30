#flask stuff
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
from sqlalchemy.pool import StaticPool

from flask import Flask, jsonify

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine("sqlite:///Resources/hawaii.sqlite",
    connect_args={'check_same_thread':False},
    poolclass=StaticPool)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>" +
        "/api/v1.0/precipitation<br/>"+
        "/api/v1.0/stations<br/>"+
        "/api/v1.0/tobs<br/>"+
        "/api/v1.0/date/<br/>"+
        "/api/v1.0/range/<br/>"
       
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_measures = list(np.ravel(results))

    return jsonify(all_measures)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >='2016-08-23').order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/date/<start>")
#, defaults={"end":None}
def by_startdate(start):
    print(start)
    """Fetch data for date."""
    if start is None:
       dateQry = 1
       #dateQry = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >=start,Measurement.date <=end).order_by(Measurement.date).all()
    else:
        #dateQry = 2
        dateQry = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >=start).order_by(Measurement.date).all()
    return jsonify(dateQry)

@app.route("/api/v1.0/range/<start>/<end>")
def by_range(start,end):
    print(start)
    """Fetch data for date."""
 
    dateQry = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >=start,Measurement.date <=end).order_by(Measurement.date).all()





    return jsonify(dateQry)


if __name__ == '__main__':
    app.run(debug=True)