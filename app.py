# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios
# https://blog.pythonanywhere.com/121/

from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="flix328",
    password="59AV8wYEq@beyN6",
    hostname="flix328.mysql.pythonanywhere-services.com",
    databasename="flix328$birds_iview"
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = "9hgnt493n);@%2n8t3)2"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    flight_paths = db.relationship("FlightPath")

class FlightPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userDB.id'))
    name = db.Column(db.String(255))
    altitude = db.Column(db.Float)
    heading = db.Column(db.Float)
    overlap = db.Column(db.Float)
    resolution = db.Column(db.String(255))
    view_angle = db.Column(db.Float)
    bird_list = db.Column(db.String(255))
    location = db.Column(db.String(255))
    zoom_level = db.Column(db.Float)
    point_list = db.Column(db.String(255))

@login_manager.user_loader
def load_user(user_id):
    #return all_users.get(user_id)
    query_data = UserDB.query.filter_by(username=user_id)
    if query_data.count() != 1:
        print("database query returned {} results, should be 1".format(query_data.count()))
    return User(user_id, query_data.first().password_hash)


class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(4096))
    size = db.Column(db.Float())

@app.route('/getBirds')
def get_birds():
    birds = Bird.query.all()
    result = ""
    for bird in birds:
        result += "{},{},".format(bird.name, bird.size)
    print("result", result)
    return jsonify(result)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
	return render_template('home.html')

# This is the function shows the plan page
@app.route('/plan', methods=["GET","POST"])
def plan():
	return render_template('plan.html')

# This is the function shows the analyse page
@app.route('/analyse', methods=["GET","POST"])
def analyse():
	return render_template('analyse.html')


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
	poly_data = [float(s) for s in request.args['poly_data'].split(',') if not (s+" ").isspace()]

	poly = Polygon()
	for i in range(0, len(poly_data), 3):
		_id = poly_data[i]
		p = Point(poly_data[i+1], poly_data[i+2])
		poly.push_end(_id, p)

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
	altitude = float(request.args['altitude'])
	heading = float(request.args['heading'])
	overlap = float(request.args['overlap'])
	resolution = request.args['resolution']
	view_angle = float(request.args['view_angle'])
	poly_data = [float(num) for num in request.args['poly_data'].split(',')]

	poly = Polygon()
	for i in range(0, len(poly_data), 3):
		_id = poly_data[i]
		p = Point(poly_data[i+1], poly_data[i+2])
		poly.push_end(_id, p)

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
#  return render_template('404.html'), 404





# This is the function that controls the main page of the web site
@app.route("/testing")
def testingindex():
    if current_user.is_authenticated:
        username_str = current_user.username
    else:
        username_str = "Log In"
    return render_template('testinghome.html', username_str=username_str)

# This is the function that holds account information
@app.route("/testingaccount/", methods=["GET","POST"])
@login_required
def testingaccount():
    username = current_user.username
    if request.method == "GET":
        return render_template('testingaccount.html', username_str=username)

    current_password = request.form["current_password"]
    if not current_user.check_password(current_password):
        return render_template('testingaccount.html', username_str=username, password_update_str="Incorrect Password")
    new_password = request.form["new_password"]
    confirm_new_password = request.form["confirm_new_password"]
    if new_password != confirm_new_password:
        return render_template('testingaccount.html', username_str=username, password_update_str="The passwords do not match")

    user = UserDB.query.filter_by(username=username)[0]
    password_hash = generate_password_hash(new_password)
    user.password_hash = password_hash
    db.session.commit()
    return render_template('testingaccount.html', username_str=username, password_update_str="Your password has been updated")

# This is the function that holds a user's files
@app.route("/testingfiles")
@login_required
def testingfiles():
    user_id = UserDB.query.filter_by(username=current_user.username).first().id
    query_data = FlightPath.query.filter_by(user_id=user_id)
    filenames = [row.name for row in query_data]

    return render_template('testingfiles.html', title="Your Files", filenames=filenames, username_str=current_user.username)

# This is the function shows the plan page
@app.route('/testingplan', methods=["GET","POST"])
@login_required
def testingplan():
	return render_template('testingplan.html', title="Untitled Plan", username_str=current_user.username)

@app.route("/testinglogin/", methods=["GET", "POST"])
def testinglogin():
    if current_user.is_authenticated:
        return redirect("/testingaccount")
    if request.method == "GET":
        return render_template("testinglogin.html")


    username = request.form["username"]
    query_data = UserDB.query.filter_by(username=username)
    if query_data.count() == 0:
        return render_template("testinglogin.html", login_error="That username is not registered")
    user = User(username, query_data[0].password_hash)

    if not user.check_password(request.form["password"]):
        return render_template("testinglogin.html", login_error="The username or password is incorrect")

    login_user(user)
    return redirect("/testingfiles")


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/testinglogin')

import emoji
def bad_username(s):
    if len(s) < 1:
        return "username must be at least 5 characters long"
    if len(s) > 20:
        return "username can be at most 20 characters long"
    has_emoji = False
    i = 0
    while(i < len(s) and not has_emoji):
        c = s[i]
        if c in emoji.UNICODE_EMOJI:
            has_emoji = True
        i += 1
    if has_emoji:
        return "username cannot contain emoji"
    return False

def bad_password(s):
    if len(s) < 5:
        return "password must be at least 5 characters long"
    if len(s) > 20:
        return "password can be at most 20 characters long"
    has_emoji = False
    i = 0
    while(i < len(s) and not has_emoji):
        c = s[i]
        if c in emoji.UNICODE_EMOJI:
            has_emoji = True
        i += 1
    if has_emoji:
        return "password cannot contain emoji"
    return False


@app.route('/testingsignup/', methods=["GET","POST"])
def testingsignup():
    if current_user.is_authenticated:
        return redirect("/testingaccount")
    if request.method == "GET":
        return render_template('testingsignup.html', username_str="Log In")

    username = request.form["username"]
    query_data = UserDB.query.filter_by(username=username)
    if query_data.count() == 1:
        return render_template("testingsignup.html", signup_error="That username is already registered")
    username_bad = bad_username(username)
    if username_bad:
        return render_template("testingsignup.html", signup_error=username_bad)
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    if password != confirm_password:
        return render_template("testingsignup.html", signup_error="The passwords do not match")
    password_bad = bad_password(password)
    if password_bad:
        return render_template("testingsignup.html", signup_error=password_bad)
    password_hash = generate_password_hash(password)
    userDB = UserDB(username=username, password_hash=password_hash)
    db.session.add(userDB)
    db.session.commit()

    user = User(username, password_hash)

    login_user(user)
    return redirect("/testingfiles")

@app.route("/testinglogout")
def logout():
    logout_user()
    return redirect("/testing")


@app.route('/savePlan')
def save_plan():
    name=request.args['name']
    altitude = request.args['altitude']
    heading = request.args['heading']
    overlap = request.args['overlap']
    resolution = request.args['resolution']
    view_angle = request.args['view_angle']
    bird_list = request.args['bird_list']
    location = request.args['location']
    zoom_level = request.args['zoom_level']
    point_list = request.args['point_list']

    #print(name, altitude, heading, overlap, resolution, view_angle, bird_list, location, zoom_level, point_list)
    user_id = UserDB.query.filter_by(username=current_user.username).first().id
    query_data = FlightPath.query.filter_by(user_id=user_id).filter_by(name=name)
    #print(UserDB.query.filter_by(username=current_user.user_id))
    #print(UserDB.query.filter_by(username=current_user.user_id).filter_by(name=name))

    assert query_data.count() < 2
    if query_data.count() == 1:
        flight_plan = query_data.first()
    else:
        flight_plan = FlightPath(user_id=user_id, name=name)


    flight_plan.altitude = altitude
    flight_plan.heading = heading
    flight_plan.overlap = overlap
    flight_plan.resolution = resolution
    flight_plan.view_angle = view_angle
    flight_plan.bird_list = bird_list
    flight_plan.location = location
    flight_plan.zoom_level = zoom_level
    flight_plan.point_list = point_list
    db.session.add(flight_plan)
    db.session.commit()

    return jsonify("")

@app.route('/deletePlan')
def delete_plan():
    name = request.args['filename']



if __name__ == "__main__":
    app.run(debug=True)