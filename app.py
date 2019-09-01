# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, render_template, jsonify, request

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
	return render_template('home.html', title="My Application")

# This is the function shows the Athletes page
@app.route('/plan', methods=["GET","POST"])
def plan():
	return render_template('plan.html', title="Planning")



# Add the "python_files" directory to sys.path to import other modules
import sys, os
CURRENT_DIRECTORY = sys.path[0]
sys.path.append(os.path.join(CURRENT_DIRECTORY, 'python_files'))

import Objects_GPS
import Objects_2D
from interface import *

# map click function happening without any refreshing
@app.route('/onMapClick')
def polygon_add():
	data = request.args['poly']
	poly = format_input_data(data)
	
	lat = float(request.args['lat'])
	lon = float(request.args['lng'])
	_id = float(request.args['_id'])
	p = Objects_2D.Point(lat, lon)
	
	poly.push(_id, p)
	return jsonify(poly.listify())




# This function deals with any missing pages and shows the Error page
#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
	app.run(debug=True)