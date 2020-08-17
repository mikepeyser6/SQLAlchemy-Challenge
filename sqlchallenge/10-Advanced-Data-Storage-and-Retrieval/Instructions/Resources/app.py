# import dependency
import numpy as np
import pandas as pd
import datetime as dt
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.abspath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# see the table
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# 2. Create an app, being sure to pass __name__
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
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    result = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    prcp_dates = []
    for date, prcp in result:
        thedict={}
        thedict[date]=prcp
        prcp_dates.append(thedict)
    session.close()    
    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    result=session.query(Station.station, Station.name).all()
    stations={}
    for stn,name in result:
        stations[stn]=name
    session.close()    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Get the last date contained in the dataset and date from one year ago
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    oneback = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # Query for dates and temperature
    result = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= oneback).\
                order_by(Measurement.date).all()
    #declare a list of Dictionary
    tobs_dates=[]
    # use for loop to get the list
    for dates, tobs in result:
        new_dict={}
        new_dict[dates]=tobs
        tobs_date_list.append(new_dict)
    #close the sission
    session.close()    
    #get the results
    return jsonify(tobs_dates)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    # create a session link from python to database
    session = Session(engine)
    #Query to get the start end date
    result = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    #close the sission
    session.close()
    #declare a list of dictionary
    return_list = {}
    # use for loop to get the list
    for min, avg, max in result:
        return_list["Start Date"]=start 
        return_list["TMIN"] = min
        return_list["TAVG"] = avg
        return_list["TMAX"] = max
    #get the results
    return jsonify(return_list)
   
@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):
    # create a session link from python to database
    session = Session(engine)
    #Query to get the start end date
    result = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= start, Measurement.date <= end).all()
    #close the sission
    session.close()
    #declare a list of dictionary
    return_list = {}
    # use for loop to get the list
    for min, avg, max in result:
        return_list["Start Date"] = start
        return_list["End Date"]= end
        return_list["TMIN"] = min
        return_list["TAVG"] = avg
        return_list["TMAX"] = max
    #get the results
    return jsonify(return_list)

if __name__ == "__main__":
    app.run(debug=True)