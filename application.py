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

user_reprompt = False
user_remprompt_2 = False

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_r'))
    return wrap

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def registration():
    return (render_template("register.html"))

@app.route("/login_r")
def login_r():
    return(render_template("login.html"))

@app.route("/registered", methods=["POST"])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    if (db.execute("SELECT username FROM users WHERE username = '%s'" % (username))).rowcount == 1:
        user_reprompt = True
        return render_template("register.html", user_reprompt=user_reprompt)
    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
        {"name": name, "username": username, "password": password})
    db.commit()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_login = request.form.get("user_login")
    pass_login = request.form.get("pass_login")
    query = "SELECT username,password FROM users WHERE username = '%s' AND password = '%s'" % (user_login, pass_login)
    if db.execute(query).rowcount == 1:
        # session[user_login] = user_login; prev
        session['user_login'] = user_login;
        session['logged_in'] = True
        return render_template("search.html")
    else:
        user_reprompt_2 = True
        return render_template("login.html", user_reprompt_2=user_reprompt_2)

@app.route("/search", methods=["POST"])
@login_required
def search():
    search_key = str(request.form.get("search"))
    # print(search_key.upper(), "this is the search key")
    result = db.execute("SELECT zipcode,city FROM zip WHERE zipcode LIKE '"+ search_key.upper() +"%' OR city LIKE '" + search_key.upper() + "%'").fetchall()
    # print(result)
    # SELECT * FROM zip WHERE city LIKE 'BOST%'
    # print("Entering For Loop")
    # for row in result:
    #     print (row[0], "this is a string")
    return render_template("search.html", result=result)

@app.route("/search/<string:zipcode>")
@login_required
def search_info(zipcode):
    retrieved_info = db.execute("SELECT * FROM zip WHERE zipcode = :zipcode", {"zipcode": str(zipcode)}).fetchone()
    if retrieved_info is None:
        # Check Rendered Template
        return render_template("failure.html")
    api_param = db.execute("SELECT lat,long FROM zip WHERE zipcode = :zipcode", {"zipcode": str(zipcode)}).fetchone()
    comment_result = db.execute("SELECT * FROM comments")
    api_key = "4dae0251077ca4b15897145e85bb08d0"
    requested = requests.get('https://api.darksky.net/forecast/' + api_key + '/' + str(api_param.lat) + ',' + str(api_param.long) + '?exclude=currently,minutely,hourly,alerts,flags')
    # print(requested.json(), "requested string")
    if requested.status_code != 200:
        raise Exception("Unsuccessful Access")
    data = requested.json()
    #WHAT OUTPUT
    print(db.execute("SELECT username FROM comments WHERE username = 'jai'").fetchall())
    #
    #current weather, time of report, textual summary, dew point, humidity as a percentage
    print(type(data), "This is a string")
    # Correct
    current_weather = data["daily"]["summary"]
    time = datetime.datetime.fromtimestamp(data["daily"]["data"][0]["time"]).strftime('%Y-%m-%d %H:%M:%S')
    temperature = data["daily"]["data"][0]["temperatureHigh"]
    dew_point = data["daily"]["data"][0]["dewPoint"]
    humidity = data["daily"]["data"][0]["humidity"] * 100
    #test

    #
    # print(current_weather, "string 15")
    # text_summary = data['summary']
    # print(current_weather, text_summary)
    return render_template("search_info.html", retrieved_info=retrieved_info, current_weather=current_weather, time=time, temperature=temperature, \
        dew_point=dew_point, humidity=humidity, comment_result=comment_result)

@app.route("/comment/<string:city>/<string:zipcode>", methods=["POST"])
@login_required
def comment(city, zipcode):
    added = request.form.get("comment_section")
    # print(session['user_login'])
    user = session['user_login']
    # db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
    #     {"name": name, "username": username, "password": password})
    check = db.execute("SELECT username,city FROM comments WHERE username='" + user + "' AND city='" + city + "'").fetchall()
    if check == None:
        db.execute("INSERT INTO comments (username, comment, place) VALUES (:username, :comment, :place)",
            {"username": session['user_login'], "comment": added, "place": city})
        search_info(zipcode)
    else:
        #add a URL template
        raise Exception("Already Commented")

@app.route("/api/<string:zipcode>")
def api_zipcode(zipcode):
    zipcode_new = db.execute("SELECT zipcode FROM zip WHERE zipcode = '" + zipcode + "'")
    if zipcode_new is None:
        return jsonify({"error": "Zip does not exist"}), 422
    zipcode_total = db.execute("SELECT * FROM zip WHERE zipcode = '" + zipcode + "'")
    return jsonify({
        "place_name": str(zipcode_total.city),
        "state": str(zipcode_total.state),
        "latitude": str(zipcode_total.lat),
        "longitude": str(zipcode_total.long),
        "zip": str(zipcode_total.zipcode),
        "population": str(zipcode_total.population)
        # ADD THE OTHER ITEM HERE
    })



if __name__ == "__main__":
    index();

#