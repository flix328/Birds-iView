# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, Response, render_template, abort

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
	return render_template('home.html', title="My Application")

# This is the function shows the Athletes page
@app.route('/plan', methods=["GET","POST"])
def plan():
	#print("jsiofjasio")
	return render_template('plan.html', title="Planning")





# background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
	print("Hello")
	return "nothing"
	



# This function deals with any missing pages and shows the Error page
#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
	app.run(debug=True)