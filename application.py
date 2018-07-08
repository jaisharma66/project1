import os

from flask import Flask, session, render_template, request
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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registered", methods=["POST"])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
        {"name": name, "username": username, "password": password})
    db.commit()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_login = request.form.get("user_login")
    pass_login = request.form.get("pass_login")
    try:
        db.execute("SELECT * FROM users WHERE ('username' = 'user_login') AND ('password' = 'pass_login')")
        print("SUCC")
    except ValueError:
        print("Item Does Not Exist")


if __name__ == "__main__":
    index();