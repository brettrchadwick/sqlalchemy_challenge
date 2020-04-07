import sqlalchemy
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
#import Flask and jsonify
from flask import Flask, jsonify

#create engine and save table references for later queries
engine=create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()
measurements=Base.classes.measurement
stations=Base.classes.station

session=Session(engine)

#flask setup

app=Flask(__name__)

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start_date).filter(measurements.date <= end_date).all()

@app.route("/")
def index():
    return(f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/<start>/end/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year=dt.date(2017, 8, 23) -dt.timedelta(days=365)
    precdata=session.query(measurements.date, measurements.prcp).filter(measurements.date>=prev_year).all()

    precresult={}
    for result in precdata:
        precresult[result[0]]=result[1]
    return jsonify(precresult)

@app.route("/api/v1.0/stations")
def stations1():
    statdata=session.query(stations.station, stations.name).all()

    stat_list={}
    for result in statdata:
        stat_list[result[0]]=result[1]
    return jsonify(stat_list)

@app.route("/api/v1.0/tobs")
def tobs():
    active_stat=session.query(measurements.station, func.count(measurements.station)).group_by(measurements.station).order_by(func.count(measurements.station).desc()).all()
    most_active=active_stat[0][0]
    temp_info=session.query(measurements.date, measurements.tobs).filter(measurements.date >= "2016-08-23").filter(measurements.station == most_active).all()
    tobsdict={}
    for result in temp_info:
        tobsdict[result[0]]=result[1]
    return jsonify(tobsdict)

    

if __name__ == '__main__':    
    app.run(debug=True)