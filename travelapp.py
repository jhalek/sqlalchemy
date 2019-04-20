import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

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
        f"/api/v1.0/start date (Format YYYY-MM-DD)<br/>"
        f"/api/v1.0/start date/end date (Format YYYY-MM-DD)"
    )

######################################

@app.route(f"/api/v1.0/precipitation")
def names():

    #Query all precip measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    #Convert list of tuples into normal list
    prcp_list = []
    
    for date, prcp in results:
        dates_prcp = {}
        dates_prcp["date"] = date
        dates_prcp["prcp"] = prcp
        prcp_list.append(dates_prcp)

    return jsonify(prcp_list)

######################################

@app.route(f"/api/v1.0/stations")
def stations():

    #Query all stations
    results = session.query(Measurement.station).distinct().all()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

######################################

@app.route(f"/api/v1.0/tobs")
def tobs():
    
    #Query dates and temp readings
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-22').all()

    #Convert list of tuples into normal list
    tobs_list = []
    
    #append data to list
    for date, tobs in results:
        dates_tobs = {}
        dates_tobs["date"] = date
        dates_tobs["tobs"] = tobs
        tobs_list.append(dates_tobs)

    return jsonify(tobs_list)

######################################

@app.route("/api/v1.0/<start>")
def start_date(start):
        
        #set variables from user input
        start_date = start
        
        #create empty list
        xlist = []

        #run queries from user inputs and return values only in matched
        min_ = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()
        if len(min_) != 0:
            xlist.append('Mintemp: '+ str(np.min(min_)))

        max_ = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()
        if len(max_) != 0:
            xlist.append('Maxtemp: '+ str(np.max(max_)))
            
        busy = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()
        if len(busy) != 0:
            xlist.append('Avg Temp: '+ str(np.mean(busy)))

        #return message to user if no date(s) are found    
        if len(xlist) == 0:
            return jsonify({"error": f"Date not found."}), 404
        
        #return json
        return jsonify(xlist)
    
######################################

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
        
        #set variables from user input
        start_date = start
        end_date = end
        
        #create empty list
        xlist = []

        #run queries from user inputs and return values only in matched
        min_ = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        if len(min_) != 0:
            xlist.append('Mintemp: '+ str(np.min(min_)))
        
        max_ = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        if len(max_) != 0:
            xlist.append('Maxtemp: '+ str(np.max(max_)))

        busy = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        if len(busy) != 0:
            xlist.append('Avg Temp: '+ str(np.mean(busy)))

        #return message to user if no date(s) are found    
        if len(xlist) == 0:
            return jsonify({"error": f"Date not found."}), 404
        
        #return json
        return jsonify(xlist)
    
######################################        

if __name__ == '__main__':
    app.run(debug=True)


