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
    
    results = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()

    all_measures = list(np.ravel(results))

    return jsonify(all_measures)


@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >='2016-08-23').order_by(Measurement.date).all()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/date/<start>")
def by_startdate(start):
    print(start)
    
    if start is None:
        dateQry = 1
    else:
        dateQry = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >=start).order_by(Measurement.date).all()
    return jsonify(dateQry)

@app.route("/api/v1.0/range/<start>/<end>")
def by_range(start,end):
    print(start)
 
    dateQry = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >=start,Measurement.date <=end).order_by(Measurement.date).all()

    return jsonify(dateQry)


if __name__ == '__main__':
    app.run(debug=True)