import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Pythonxd=ds  to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the home page

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    f"Here are the routes that are available<br/>"
    f"Click the name of the route to go that route</br>"
    f"<a href=\"/api/v1.0/precipitation\">Precipitation Data</a><br/>"
    f"<a href=\"/api/v1.0/stations\">Station Data</a><br/>"
    f"<a href=\"/api/v1.0/tobs\">TOBS Data</a><br/>"
    f"<a href=\"/api/v1.0/<start_date>\">TOBS Data by date</a>(Min, Max and Avg) \
        of all dates greater than and equal to the start date. \
        Enter your desired date at the end of the URL (YYYY-MM-DD).\
        Data dates range from 2010-01-01 to 2017-08-23<br/>"
    f"<a href=\"/api/v1.0/<start_date>/<end_date>\">TOBS Data by dates</a>(Min, Max and Avg) \
        of all dates between your start date and end date. \
        Enter your desired dates at the end of the URL (YYYY-MM-DD/YYYY-MM-DD).\
        Data dates range from 2010-01-01 to 2017-08-23<br/><br/>"
    )
    
# 4. Define our routes and display user their options

@app.route("/api/v1.0/precipitation")
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
def precipitation():
    print("Server received request for precipitation page...")
    session = Session(engine)
    precip_query = (session.query(Measurement.date, Measurement.prcp)
                          .filter(Measurement.date > '2016-08-23')
                          .all())
    precip_dict = {}
    for date, measurement in precip_query:
        precip_dict[date] = measurement
    
    return jsonify(precip_dict)
    

@app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset.

def stations():
    print("Server received request for stations page...")
    session = Session(engine)
    stations_counts = list(session.query(Measurement.station)\
                                     .group_by(Measurement.station)\
                                     .all())
    stations_counts_list = []
    for station in stations_counts:
        stations_counts_list.append(station[0])
    return jsonify(stations_counts_list)


@app.route("/api/v1.0/tobs")
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

def tobs():
    print("Server received request for tobs page...")
    session = Session(engine)
    last_12_months_of_tobs_data = (session.query(Measurement.date, Measurement.tobs)
                                    .filter(Measurement.date > '2016-08-23')
                                    .all())
    return jsonify(last_12_months_of_tobs_data)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start_date>")
# When given the start only, calculate TMIN, TAVG, and TMAX for 
# all dates greater than and equal to the start date.

def start_date(start_date):
    print("Server received request for start date page...")
    session = Session(engine)
    tobs_start_date_only = (session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
                                   func.avg(Measurement.tobs))
                                  .filter(Measurement.date >= start_date)
                                  .all())
    
    return jsonify(tobs_start_date_only)


@app.route("/api/v1.0/<start_date>/<end_date>")
# When given the start and the end date, 
# calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

def end(start_date,end_date):
    print("Server received request for start/end date page...")    
    session = Session(engine)
    tobs_start_date_end_date = (session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
                                   func.avg(Measurement.tobs))
                                  .filter(Measurement.date >= start_date)
                                  .filter(Measurement.date <= end_date)
                                  .all())
    
    return jsonify(tobs_start_date_end_date)


if __name__ == "__main__":
    app.run(debug=True)
