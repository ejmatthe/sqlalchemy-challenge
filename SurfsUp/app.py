# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Hello, here are the following paths: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Start session
    session = Session(engine)
    # Run query
    sel_precip = [Measurement.date,
          Measurement.prcp]
    last_year = session.query(*sel_precip).filter(func.strftime(Measurement.date) >= (dt.date(2017, 8, 23) - dt.timedelta(days=365))).all()
    # Set up list to store dict in at end of loop to jsonify
    last_year_precipitation = []
    for date, prcp in last_year:
        rain_dict = {}
        rain_dict[date] = prcp
        last_year_precipitation.append(rain_dict)
    return jsonify(last_year_precipitation)
    # Close session
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    # Start session
    session = Session(engine)
    # Run query
    sel_stations = [Measurement.station,
        func.count()]
    station_count = session.query(*sel_stations).group_by(Measurement.station).order_by(func.count().desc()).all()
    # Set up list to store dict in at end of loop to jsonify
    station_list = []
    for site in station_count:
        station_list.append(site[0])
    return jsonify(station_list)
    # Close session
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Start session
    session = Session(engine)
    # Run query
    sel_tobs = [Measurement.date,
        Measurement.tobs]
    annual_station = session.query(*sel_tobs).\
            filter(func.strftime(Measurement.date) >= (dt.date(2017, 8, 23) - dt.\
            timedelta(days=365))).filter(Measurement.station == "USC00519281").all()
    # Set up list to store dict in at end of loop to jsonify
    annual_data = []
    for date, tobs in annual_station:
        annual_dict = {}
        annual_dict[date] = tobs
        annual_data.append(annual_dict)
    return jsonify(annual_data)
    # Close session
    session.close()

@app.route("/api/v1.0/<start>")
def start(start):
    # Start session
    session = Session(engine)
    # Run query
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    # Set up list to store dict in at end of loop to jsonify
    start_tobs = []
    for min, avg, max in temps:
        start_tobs_dict = {}
        start_tobs_dict["min_temp"] = min
        start_tobs_dict["avg_temp"] = avg
        start_tobs_dict["max_temp"] = max
        start_tobs.append(start_tobs_dict)
    return jsonify(start_tobs)
    # Close session
    session.close()


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Start session
    session = Session(engine)
    # Run query
    end_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Set up list to store dict in at end of loop to jsonify
    end_tobs = []
    for min, avg, max in end_temps:
        end_tobs_dict = {}
        end_tobs_dict["min_temp"] = min
        end_tobs_dict["avg_temp"] = avg
        end_tobs_dict["max_temp"] = max
        end_tobs.append(end_tobs_dict)
    return jsonify(end_tobs)
    # Close session
    session.close()

if __name__ == "__main__":
    app.run(debug=True)