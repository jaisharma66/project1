# Import statements
import os
import requests
import datetime

from flask import Flask, session, render_template, request, flash, g, redirect, url_for, json, jsonify
from functools import wraps
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Boolean variables used to check login reprompt
user_reprompt = False
user_remprompt_2 = False

# Requires login for certain parts of website
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_r'))
    return wrap

# Main Page
@app.route("/")
def index():
    return render_template("index.html")

# Registration page if some fields are not given (referred to by other files)
@app.route("/registration")
def registration():
    return (render_template("register.html"))

# Registration Page
@app.route("/registered", methods=["POST"])
def register():
    # Variables from form
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    # If checking whether user needs to be repromoted
    if (db.execute("SELECT username FROM users WHERE username = '%s'" % (username))).rowcount == 1:
        user_reprompt = True
        return render_template("register.html", user_reprompt=user_reprompt)

    # Inserts user data into table in SQL
    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
        {"name": name, "username": username, "password": password})
    db.commit()
    return render_template("login.html")

# Login redirect if incorrect login is given
@app.route("/login_r")
def login_r():
    return(render_template("login.html"))

# Login Page
@app.route("/login", methods=["POST"])
def login():
    # Variables from form
    user_login = request.form.get("user_login")
    pass_login = request.form.get("pass_login")

    # Database query checking to see if user login exists and checks out
    query = "SELECT username,password FROM users WHERE username = '%s' AND password = '%s'" % (user_login, pass_login)
    if db.execute(query).rowcount == 1:
        session['user_login'] = user_login;
        session['logged_in'] = True
        return render_template("search.html")
    else:
        user_reprompt_2 = True
        return render_template("login.html", user_reprompt_2=user_reprompt_2)

# Logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("index.html")

# Search Page
@app.route("/search", methods=["POST"])
@login_required
def search():
    # Variables from form
    search_key = str(request.form.get("search"))
    result = db.execute("SELECT zipcode,city FROM zip WHERE zipcode LIKE '"+ search_key.upper() +"%' OR city LIKE '" + search_key.upper() + "%'").fetchall()
    return render_template("search.html", result=result)

# Checks details of the search, displays values
@app.route("/search/<string:zipcode>")
@login_required
def search_info(zipcode):
    # Information recieved through zipcode of /search, if statement checks to see if zip exists
    retrieved_info = db.execute("SELECT * FROM zip WHERE zipcode = :zipcode", {"zipcode": str(zipcode)}).fetchone()
    if retrieved_info is None:
        raise Exception("Error, no such zipcode!")

    # API parameters used for concatenated string API key
    api_param = db.execute("SELECT lat,long FROM zip WHERE zipcode = :zipcode", {"zipcode": str(zipcode)}).fetchone()
    comment_result = db.execute("SELECT * FROM comments WHERE place = '" + zipcode + "'").fetchone()
    api_key = "4dae0251077ca4b15897145e85bb08d0"
    requested = requests.get('https://api.darksky.net/forecast/' + api_key + '/' + str(api_param.lat) + ',' + str(api_param.long) + '?exclude=currently,minutely,hourly,alerts,flags')
    if requested.status_code != 200:
        raise Exception("Unsuccessful Access")

    # Data JSON conversion, passed in to HTML sheet for viewing
    data = requested.json()
    current_weather = data["daily"]["summary"]
    time = datetime.datetime.fromtimestamp(data["daily"]["data"][0]["time"]).strftime('%Y-%m-%d %H:%M:%S')
    temperature = data["daily"]["data"][0]["temperatureHigh"]
    dew_point = data["daily"]["data"][0]["dewPoint"]
    humidity = data["daily"]["data"][0]["humidity"] * 100
    return render_template("search_info.html", retrieved_info=retrieved_info, current_weather=current_weather, time=time, temperature=temperature, \
        dew_point=dew_point, humidity=humidity, comment_result=comment_result)

# Adds Comment to Search
@app.route("/comment/<string:zipcode>", methods=["POST"])
@login_required
def comment(zipcode):
    # Variables from form
    added = request.form.get("comment_section")
    user = session['user_login']

    #Database check if user has commented
    check = db.execute("SELECT username,place FROM comments WHERE username='" + user + "' AND place='" + zipcode + "'").fetchall()
    if check == []:
        db.execute("INSERT INTO comments (username, comment, place) VALUES (:username, :comment, :place)", {"username": session['user_login'], "comment": added, "place": zipcode})
        db.commit()
        return redirect(url_for("search_info", zipcode=zipcode))
    else:
        raise Exception("Already Commented")

# API access
@app.route("/api/<string:zipcode>")
def api_zipcode(zipcode):
    zipcode_new = db.execute("SELECT zipcode FROM zip WHERE zipcode = '" + zipcode + "'")
    if zipcode_new is None:
        return jsonify({"error": "Zip does not exist"}), 422
    zipcode_total = db.execute("SELECT * FROM zip WHERE zipcode = '" + zipcode + "'").fetchone()
    return jsonify({
        "place_name": str(zipcode_total.city),
        "state": str(zipcode_total.state),
        "latitude": str(zipcode_total.lat),
        "longitude": str(zipcode_total.long),
        "zip": str(zipcode_total.zipcode),
        "population": str(zipcode_total.population)
    })

if __name__ == "__main__":
    index();