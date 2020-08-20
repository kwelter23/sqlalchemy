import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#Flask setup
app = Flask(__name__)


#Create and apps
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
    )

#Precipitation Dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

     # Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close

    # Create a dictionary from the row data and append to a list 
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)


#All Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#Temperatures for most active station
@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all Dates and Temp for MOST active station
    sel = [Measurement.date, 
           Measurement.tobs]
    results = session.query(*sel).\
        filter(Measurement.station == 'USC00519281').\
        filter(func.strftime(Measurement.date) > '2016-08-23').\
        order_by(Measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    most_observed_temps = list(np.ravel(results))

    return jsonify(most_observed_temps)

#Minimum Temperature, average temperature and max temperature for a date range


    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )







if __name__ == "__main__":
    app.run(debug=True)