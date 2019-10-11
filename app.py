# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="flix328",
    password="59AV8wYEq@beyN6",
    hostname="flix328.mysql.pythonanywhere-services.com",
    databasename="flix328$birds"
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
birds_db = SQLAlchemy(app)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
	return render_template('home.html', title="My Application")

# This is the function shows the plan page
@app.route('/plan', methods=["GET","POST"])
def plan():
	return render_template('plan.html', title="Planning")

# This is the function shows the analyse page
@app.route('/analyse', methods=["GET","POST"])
def analyse():
	return render_template('analyse.html', title="Analysis")


# Add the "python_files" directory to sys.path to import other modules
import sys, os
CURRENT_DIRECTORY = sys.path[0]
sys.path.append(os.path.join(CURRENT_DIRECTORY, 'python_files'))

import Objects_GPS
import Objects_2D
from plan_flight import *
from earth_view import *
from interface import *

# map click function happening without any refreshing
@app.route('/onMapClick')
def polygon_add():
	data = request.args['poly']
	altitude, heading, overlap, resolution, view_angle, poly = format_input_data(data)

	lat = float(request.args['lat'])
	lon = float(request.args['lng'])
	_id = float(request.args['_id'])
	p = Objects_2D.Point(lat, lon)

	poly.push(_id, p)
	return jsonify(poly.listify())

MAX_POINTS = 99
# get new flight path
@app.route('/updatePath')
def get_path():
	data = request.args['data']
	altitude, heading, overlap, resolution, view_angle, poly = format_input_data(data)

	gs = [Objects_GPS.Point(lat, lng) for _, lat, lng in poly.listify()]
	# convert GPS points to 2D points
	p3Ds = [gps_to_xyz(g) for g in gs]
	p_r = EARTH.project(centre_point(p3Ds))
	ps = [xyz_to_xy(p_r, p) for p in p3Ds]

	camera = {"view angle": view_angle, "resolution": resolution}

	flight_plan = generate_flight_plan(ps, camera, altitude, overlap, heading, max_points=MAX_POINTS)

	poly_2D = [xyz_to_xy(p_r, gps_to_xyz(Objects_GPS.Point(lat, lon))) for _, lat, lon in poly.listify()]

	total = 0
	for p1_num, p1 in enumerate(poly_2D):
		p0 = poly_2D[p1_num - 1]
		total += p0.x * p1.y - p1.x * p0.y
	area = 0.5 * abs(total)

	dist = flight_path_dist(flight_plan[:MAX_POINTS])
	num_photos = len(flight_plan)

	result = "{}, {}, {}".format(area, dist, num_photos)
	for p in flight_plan:
		g = xy_to_gps(p_r, p)
		result += ", " + str(g.lat) + ", " + str(g.lon)
	return jsonify(result)


# This function deals with any missing pages and shows the Error page
#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html', title="404"), 404

app.run(debug=True)