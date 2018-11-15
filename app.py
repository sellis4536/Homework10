import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Set engine, create engine accessing hawaii.sqlite in resources subdir -- apply connect_arg to allow multiple threads (bad practice per Instr.)
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False},)

# reflect existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
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
        f"Available Routes:<p/>"
        f"/api/v1.0/precipitation<br/>"
        f" Returns Listing of Date and Precipitation for 12 month range<p/>"
        f"/api/v1.0/stations<br/>"  
        f"Returns Listing of Hawaii Weather Stations<p/>"
        f"/api/v1.0/tobs<br/>"
        f"Returns Listing of Temp. Observations (tobs) for 12 month range<p/>"
        f"/api/v1.0/summary_start<br/>"
        f" Return Min, Avg and Max Temps from 2017-05-10 forward<p/>"
        f"/api/v1.0/summary_range<br/>"
        f"Returns Min, Avg and Max Temps for 2017-05-10 to 2017-05-20<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns listing of date and precipitation for 12 month range"""
    results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date <= '2017-08-23').\
                        filter(Measurement.date >= '2016-08-23').all()
                        
    #ravel method initially used and discarded -- datePrecip = list(np.ravel(results)) #ravel attempts to convert matrix into flat list
    # Convert the query results into a dictionary with KVP date:prcp
    datePrcp = []
    for result in results:
        datePrcpDict = {}
        datePrcpDict["date"] = result[0]
        datePrcpDict["prcp"] = result[1]
        datePrcp.append(datePrcpDict)
    return jsonify(datePrcp)


@app.route("/api/v1.0/stations")
def stations():
    """Returns a listing of Hawaii Weather Stations"""
    results = session.query(Station.station, Station.name).all()
     #ravel method initially used and discarded -- stationRavel = list(np.ravel(results)) #ravel attempts to convert matrix into flat list
    staName = []
    for result in results:
        staNameDict = {}
        staNameDict["station"] = result[0]
        staNameDict["name"] = result[1]
        staName.append(staNameDict)
    return jsonify(staName)


@app.route("/api/v1.0/tobs")
def tobs():
    """Returns Listing of Temp. Observations (tobs) for 12 month range based on last datapoint (USC00516128, 2017-08-23)"""
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date <= '2017-08-23').\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00516128').all()
     #ravel method initially used and discarded -- tobsRavel = list(np.ravel(results))
    dateTobs = []
    for result in results:
        tobsDict = {}
        tobsDict["date"] = result[0]
        tobsDict["tobs"] = result[1]
        dateTobs.append(tobsDict)
    return jsonify(dateTobs)


@app.route("/api/v1.0/summary_start")
def summary_start():
    """Return a list of Min, Avg and Max Temps (tobs) from start date through most recent available tobs date"""

    results = session.query(func.min(Measurement.tobs),\
                func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= '2017-05-10').all()

    
    startTobs = list(np.ravel(results))

    return jsonify(startTobs)

@app.route("/api/v1.0/summary_range")
def summary_range():
    """Return a list of Min, Avg and Max Temps (tobs) from start date through end date"""

    results = session.query(func.min(Measurement.tobs),\
                func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= '2017-05-10').\
                        filter(Measurement.date <= '2017-05-20').all()
    
    rangeTobs = list(np.ravel(results))

    return jsonify(rangeTobs)

    
if __name__ == '__main__':
    app.run(debug=True)
