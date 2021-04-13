import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np

#-----------------------------------------------------
# Setup Database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

meas = Base.classes.measurement
stat = Base.classes.station
#-----------------------------------------------------
# Flask setup and homepage route
app = Flask(__name__)

@app.route('/')
def home_page():
    return (
        f'Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start><end>'
    )

#--------------------------------------------------------
# Precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():

    session = Session(engine)

    prcp_query = session.query(meas.date, meas.prcp).filter(meas.date > '2016-08-23').filter(meas.date <= '2017-08-23').order_by(meas.date).all()

    session.close()

# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary

    prcp_dict = {}
    for date, prcp in prcp_query:
        prcp_dict[date] = prcp
        
    return jsonify(prcp_dict)
#--------------------------------------------------------
# Station route
@app.route("/api/v1.0/stations")
def stations():

# Return a JSON list of stations from the dataset.    
    session = Session(engine)
    
    results = session.query(stat.station).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)
#--------------------------------------------------------
# Temperature observations route
@app.route('/api/v1.0/tobs')
def tobs():

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

    session = Session(engine)

    temp_query = session.query(meas.date, meas.tobs, meas.station).\
    filter(meas.date > '2016-08-23').filter(meas.date <= '2017-08-23').\
    filter(meas.station == 'USC00519281').order_by(meas.date).all()

    session.close()


  # Create a dictionary from the row data and append to a list
    temp_list = []
    for date, tobs, station in temp_query:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = tobs
        temp_dict["station"] = station
        temp_list.append(temp_dict)

    return jsonify(temp_list)
#--------------------------------------------------------
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>')
def start_date(start):

    # Define TMIN, MAX, and TAVG
    TMIN = func.min(meas.tobs)
    TMAX = func.max(meas.tobs)
    TAVG = func.avg(meas.tobs)
 
    # Query Results
    session = Session(engine)
    
    results = session.query(meas.date, TMIN, TMAX, TAVG).filter(meas.date > '2016-08-23').order_by(meas.date).all()
      
    session.close()

    # Create a dictionary from the row data and append to a list
    all_TMIN = []
    for date, TMIN, TMAX, TAVG in results:
        TMIN_dict = {}
        TMIN_dict[f"{date}"] = TMIN, TMAX, TAVG
        all_TMIN.append(TMIN_dict)

    return jsonify(all_TMIN)
#--------------------------------------------------------
@app.route('/api/v1.0/<start><end>')
def start_end_date(start, end):

    # Define TMIN, MAX, and TAVG
    TMIN = func.min(meas.tobs)
    TMAX = func.max(meas.tobs)
    TAVG = func.avg(meas.tobs)
 
    # Query Results
    session = Session(engine)

    results = session.query(meas.date, TMIN, TMAX, TAVG).filter(meas.date > '2016-08-23').filter(meas.date < '2016-09-23').order_by(meas.date).all()
      
    session.close()

    # Create a dictionary from the row data and append to a list
    all_start_end = []
    for date, TMIN, TMAX, TAVG in results:
        start_end_dict = {}
        start_end_dict[f"{date}"] = TMIN, TMAX, TAVG
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)
#--------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)







