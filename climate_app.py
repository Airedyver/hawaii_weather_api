# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, MetaData, Table , distinct
import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sqlalchemy import *

from flask import Flask , jsonify

app = Flask("my_great_app")




#select trip dates, specifically because my birthday is in this range
trip_start_date = '2018-02-05'                                               
trip_end_date = '2018-02-20'

# Create engine using the `demographics.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# Collect the names of tables within the database
inspector.get_table_names()

meta = MetaData()
meas_table = Table('clean_hawaii_measurements', meta)
stats_table = Table('clean_hawaii_stations', meta)
insp = inspector.from_engine(engine)
insp.reflecttable(meas_table, None)
insp.reflecttable(stats_table, None)

columns = inspector.get_columns('clean_hawaii_measurements')
for column in columns:
    print(column)

columns = inspector.get_columns('clean_hawaii_stations')
for column in columns:
    print(column)

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()

conn = engine.connect()                                                     
inspector = inspect(engine)      

# Assign the hawaii_measurement class to a variable called `Measurement`
Measurement = Base.classes.clean_hawaii_measurements

# Assign the hawaii_station class to a variable called `Station`
Station = Base.classes.clean_hawaii_stations

# Create a session
session = Session(engine)






@app.route('/api/v1.0/precipitation')
def precipitation():
	# queries the database for previous years precipitation data.
	prcp_anyl = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <='2017-08-23').filter(Measurement.date >='2016-08-24').all()

	prcp_df = pd.DataFrame(prcp_anyl)

	#prcp_df['date'] = pd.to_datetime(prcp_df['date'])

	prcp_date = prcp_df.set_index('date')

	return jsonify(prcp_date.to_dict()['prcp'])

@app.route('/api/v1.0/stations')
def stations():
	stats = session.query(Station.name)
	return "jsonify(stats)

@app.route('/contact')
def contact():
	return "Welcome to the contact page"
if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug=True)