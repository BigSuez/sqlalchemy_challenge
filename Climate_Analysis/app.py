# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
################################################# 
@app.route('/')
def homepage():
    return 'Available Routes:</br>\
            /api/v1.0/precipitation - Precipitation Data for past 12 Months</br>\
            /api/v1.0/stations - List of stations</br>\
            /api/v1.0/tobs - Temperatures last 12 months</br>\
            /api/v1.0/[start] - Avg, Min, Max Temperatures since start date (YYYY-MM-DD)</br>\
            /api/v1.0/[start]/[end] - Avg, Min, Max Temperatures from Start to End Date (YYYY-MM-DD)'

@app.route('/api/v1.0/precipitation')
def precip():
    last_year_list = session.query(Measurement.date, Measurement.prcp).all()
    last_year_dict = {}
    for row in last_year_list:
      last_year_dict.update({row[0]:row[1]})
    return last_year_dict

@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    stations = [tuple(row) for row in stations]
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    year_ago = dt.date(2016, 8, 23)
    last_year_active = session.query(Measurement.date, Measurement.tobs)\
                            .filter(Measurement.station == 'USC00519281')\
                            .filter(Measurement.date > year_ago).all()
    last_year_active = [tuple(row) for row in last_year_active]
    return jsonify(last_year_active)

@app.route('/api/v1.0/<start>')
def byStart(start):
    end='2017-08-23'
    selected = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                             func.max(Measurement.tobs))\
                             .filter(Measurement.date > start)\
                             .filter(Measurement.date < end)
    selected = [tuple(row) for row in selected]
    return jsonify(selected)

@app.route('/api/v1.0/<start>/<end>')
def byRange(start, end):
    selected = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                             func.max(Measurement.tobs))\
                             .filter(Measurement.date > start)\
                             .filter(Measurement.date < end)
    selected = [tuple(row) for row in selected]
    return jsonify(selected)

if __name__ == '__main__':
    app.run(debug=True)
